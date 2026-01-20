from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from localvault.crypto import KdfParams
from localvault.storage import EncryptedStorage


@dataclass
class Workspace:
    root: Path
    storage: EncryptedStorage

    @property
    def vault_dir(self) -> Path:
        return self.root / ".vault"

    @property
    def spaces_dir(self) -> Path:
        return self.root / "spaces"

    @property
    def attachments_dir(self) -> Path:
        return self.root / "attachments"

    def init_layout(self) -> None:
        (self.vault_dir / "index").mkdir(parents=True, exist_ok=True)
        (self.vault_dir / "cache" / "thumbs").mkdir(parents=True, exist_ok=True)
        self.spaces_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)

    def write_metadata(self, spaces: list[str] | None = None) -> None:
        spaces = spaces or []
        meta = {
            "workspaceId": f"ws-{uuid.uuid4().hex[:6]}",
            "created": datetime.now(timezone.utc).isoformat(),
            "spaces": spaces,
            "version": 1,
        }
        meta_path = self.vault_dir / "vault.meta.json.enc"
        self.storage.write(meta_path, json.dumps(meta, indent=2).encode("utf-8"))

    def write_keyinfo(self, kdf_params: KdfParams, salt_b64: str, version: int = 1) -> None:
        keyinfo = {
            "version": version,
            "kdf": kdf_params.to_dict(),
            "salt": salt_b64,
        }
        keyinfo_path = self.vault_dir / "vault.keyinfo.json"
        keyinfo_path.write_text(json.dumps(keyinfo, indent=2), encoding="utf-8")
