from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"LVLT1"
VERSION = 1


@dataclass(frozen=True)
class KdfParams:
    time_cost: int = 3
    memory_cost_kib: int = 2**16
    parallelism: int = 2
    hash_len: int = 32

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time_cost": self.time_cost,
            "memory_cost_kib": self.memory_cost_kib,
            "parallelism": self.parallelism,
            "hash_len": self.hash_len,
        }


@dataclass(frozen=True)
class EncryptionHeader:
    kdf: KdfParams
    salt: bytes
    wrap_nonce: bytes
    wrapped_key: bytes
    data_nonce: bytes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": VERSION,
            "kdf": self.kdf.to_dict(),
            "salt": base64.b64encode(self.salt).decode("utf-8"),
            "wrap_nonce": base64.b64encode(self.wrap_nonce).decode("utf-8"),
            "wrapped_key": base64.b64encode(self.wrapped_key).decode("utf-8"),
            "data_nonce": base64.b64encode(self.data_nonce).decode("utf-8"),
            "aead": "AES-256-GCM",
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EncryptionHeader":
        kdf_data = data["kdf"]
        return EncryptionHeader(
            kdf=KdfParams(
                time_cost=int(kdf_data["time_cost"]),
                memory_cost_kib=int(kdf_data["memory_cost_kib"]),
                parallelism=int(kdf_data["parallelism"]),
                hash_len=int(kdf_data["hash_len"]),
            ),
            salt=base64.b64decode(data["salt"]),
            wrap_nonce=base64.b64decode(data["wrap_nonce"]),
            wrapped_key=base64.b64decode(data["wrapped_key"]),
            data_nonce=base64.b64decode(data["data_nonce"]),
        )


def derive_master_key(passphrase: str, salt: bytes, kdf: KdfParams) -> bytes:
    return hash_secret_raw(
        secret=passphrase.encode("utf-8"),
        salt=salt,
        time_cost=kdf.time_cost,
        memory_cost=kdf.memory_cost_kib,
        parallelism=kdf.parallelism,
        hash_len=kdf.hash_len,
        type=Type.ID,
    )


def encrypt_bytes(plaintext: bytes, passphrase: str, kdf: KdfParams | None = None) -> bytes:
    kdf = kdf or KdfParams()
    salt = os.urandom(16)
    master_key = derive_master_key(passphrase, salt, kdf)

    data_key = os.urandom(32)
    wrap_nonce = os.urandom(12)
    wrapped_key = AESGCM(master_key).encrypt(wrap_nonce, data_key, None)

    data_nonce = os.urandom(12)
    ciphertext = AESGCM(data_key).encrypt(data_nonce, plaintext, None)

    header = EncryptionHeader(
        kdf=kdf,
        salt=salt,
        wrap_nonce=wrap_nonce,
        wrapped_key=wrapped_key,
        data_nonce=data_nonce,
    )
    header_bytes = json.dumps(header.to_dict(), separators=(",", ":")).encode("utf-8")
    header_len = len(header_bytes).to_bytes(4, "big")

    return b"".join([MAGIC, header_len, header_bytes, ciphertext])


def decrypt_bytes(payload: bytes, passphrase: str) -> bytes:
    if not payload.startswith(MAGIC):
        raise ValueError("Invalid magic header")

    header_len = int.from_bytes(payload[len(MAGIC) : len(MAGIC) + 4], "big")
    header_start = len(MAGIC) + 4
    header_end = header_start + header_len
    header = json.loads(payload[header_start:header_end].decode("utf-8"))

    if header.get("version") != VERSION:
        raise ValueError("Unsupported version")

    parsed = EncryptionHeader.from_dict(header)
    master_key = derive_master_key(passphrase, parsed.salt, parsed.kdf)
    data_key = AESGCM(master_key).decrypt(parsed.wrap_nonce, parsed.wrapped_key, None)
    ciphertext = payload[header_end:]
    return AESGCM(data_key).decrypt(parsed.data_nonce, ciphertext, None)
