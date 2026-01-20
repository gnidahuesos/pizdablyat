from __future__ import annotations

from pathlib import Path

from localvault.crypto import decrypt_bytes, encrypt_bytes


class EncryptedStorage:
    def __init__(self, passphrase: str) -> None:
        self._passphrase = passphrase

    def write(self, path: Path, plaintext: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        encrypted = encrypt_bytes(plaintext, self._passphrase)
        path.write_bytes(encrypted)

    def read(self, path: Path) -> bytes:
        payload = path.read_bytes()
        return decrypt_bytes(payload, self._passphrase)
