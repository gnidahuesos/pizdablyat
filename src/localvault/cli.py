from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path

from localvault.crypto import KdfParams
from localvault.storage import EncryptedStorage
from localvault.workspace import Workspace


def _init_workspace(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    storage = EncryptedStorage(args.passphrase)
    workspace = Workspace(root=root, storage=storage)
    workspace.init_layout()
    workspace.write_metadata(spaces=args.spaces)
    salt_b64 = base64.b64encode(os.urandom(16)).decode("utf-8")
    workspace.write_keyinfo(KdfParams(), salt_b64)
    print(f"Workspace initialized at {root}")


def _encrypt_file(args: argparse.Namespace) -> None:
    storage = EncryptedStorage(args.passphrase)
    plaintext = Path(args.input).read_bytes()
    output = Path(args.output)
    storage.write(output, plaintext)
    print(f"Encrypted {args.input} -> {args.output}")


def _decrypt_file(args: argparse.Namespace) -> None:
    storage = EncryptedStorage(args.passphrase)
    plaintext = storage.read(Path(args.input))
    Path(args.output).write_bytes(plaintext)
    print(f"Decrypted {args.input} -> {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="localvault")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize a workspace")
    init.add_argument("path", help="workspace directory")
    init.add_argument("--passphrase", required=True, help="workspace passphrase")
    init.add_argument("--spaces", nargs="*", default=[], help="initial spaces")
    init.set_defaults(func=_init_workspace)

    enc = sub.add_parser("encrypt", help="encrypt a file")
    enc.add_argument("input", help="input plaintext file")
    enc.add_argument("output", help="output encrypted file")
    enc.add_argument("--passphrase", required=True)
    enc.set_defaults(func=_encrypt_file)

    dec = sub.add_parser("decrypt", help="decrypt a file")
    dec.add_argument("input", help="input encrypted file")
    dec.add_argument("output", help="output plaintext file")
    dec.add_argument("--passphrase", required=True)
    dec.set_defaults(func=_decrypt_file)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
