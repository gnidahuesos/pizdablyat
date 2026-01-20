from __future__ import annotations

import base64
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from localvault.crypto import KdfParams, decrypt_bytes, encrypt_bytes
from localvault.storage import EncryptedStorage
from localvault.workspace import Workspace


class LocalVaultHandler(BaseHTTPRequestHandler):
    ui_root = Path(__file__).parent / "ui"

    def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(body.decode("utf-8"))

    def _serve_file(self, path: Path) -> None:
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        content = path.read_bytes()
        content_type, _ = mimetypes.guess_type(str(path))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in {"/", ""}:
            return self._serve_file(self.ui_root / "index.html")
        target = (self.ui_root / path.lstrip("/")).resolve()
        if not str(target).startswith(str(self.ui_root.resolve())):
            self.send_error(HTTPStatus.FORBIDDEN, "Invalid path")
            return
        self._serve_file(target)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/encrypt":
            payload = self._read_json()
            passphrase = payload.get("passphrase", "")
            plaintext = payload.get("plaintext", "")
            encrypted = encrypt_bytes(plaintext.encode("utf-8"), passphrase)
            encoded = base64.b64encode(encrypted).decode("utf-8")
            return self._send_json({"payload": encoded})
        if self.path == "/api/decrypt":
            payload = self._read_json()
            passphrase = payload.get("passphrase", "")
            encoded = payload.get("payload", "")
            raw = base64.b64decode(encoded)
            plaintext = decrypt_bytes(raw, passphrase).decode("utf-8")
            return self._send_json({"plaintext": plaintext})
        if self.path == "/api/init":
            payload = self._read_json()
            root = Path(payload.get("path", "")).expanduser().resolve()
            passphrase = payload.get("passphrase", "")
            spaces = payload.get("spaces", [])
            storage = EncryptedStorage(passphrase)
            workspace = Workspace(root=root, storage=storage)
            workspace.init_layout()
            workspace.write_metadata(spaces=spaces)
            salt_b64 = base64.b64encode(os.urandom(16)).decode("utf-8")
            workspace.write_keyinfo(KdfParams(), salt_b64)
            return self._send_json({"status": "ok", "path": str(root)})
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), LocalVaultHandler)
    print(f"LocalVault UI running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
