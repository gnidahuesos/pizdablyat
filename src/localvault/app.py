from __future__ import annotations

import base64
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path

from localvault.crypto import KdfParams, decrypt_bytes, encrypt_bytes
from localvault.storage import EncryptedStorage
from localvault.workspace import Workspace


class LocalVaultApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("LocalVault")
        self.root.geometry("980x720")
        self.root.configure(bg="#0b0f1c")
        self._configure_style()
        self._build_layout()

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Glass.TFrame",
            background="#0f1629",
            borderwidth=1,
            relief="ridge",
        )
        style.configure(
            "Glass.TLabel",
            background="#0f1629",
            foreground="#f4f7ff",
            font=("Helvetica", 11),
        )
        style.configure(
            "GlassTitle.TLabel",
            background="#0f1629",
            foreground="#f4f7ff",
            font=("Helvetica", 18, "bold"),
        )
        style.configure(
            "Glass.TButton",
            background="#7ed0ff",
            foreground="#0b0f1c",
            font=("Helvetica", 11, "bold"),
            padding=(10, 6),
        )
        style.map(
            "Glass.TButton",
            background=[("active", "#9b7bff")],
        )

    def _build_layout(self) -> None:
        header = ttk.Frame(self.root, padding=20, style="Glass.TFrame")
        header.pack(fill="x", padx=24, pady=24)

        title = ttk.Label(header, text="LocalVault", style="GlassTitle.TLabel")
        title.pack(anchor="w")
        subtitle = ttk.Label(
            header,
            text="Desktop app for encrypted, local-first workspaces (glassmorphism iOS 26 inspired).",
            style="Glass.TLabel",
        )
        subtitle.pack(anchor="w", pady=(8, 0))

        content = ttk.Frame(self.root, padding=12, style="Glass.TFrame")
        content.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        left = ttk.Frame(content, padding=16, style="Glass.TFrame")
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right = ttk.Frame(content, padding=16, style="Glass.TFrame")
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        self._build_workspace_panel(left)
        self._build_encrypt_panel(right)

        self.status = ttk.Label(self.root, text="Ready", style="Glass.TLabel")
        self.status.pack(fill="x", padx=24, pady=(0, 24))

    def _build_workspace_panel(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Workspace Setup", style="GlassTitle.TLabel").pack(anchor="w")

        form = ttk.Frame(parent, padding=12, style="Glass.TFrame")
        form.pack(fill="x", pady=(12, 0))

        ttk.Label(form, text="Path", style="Glass.TLabel").grid(row=0, column=0, sticky="w")
        self.workspace_path = tk.Entry(form)
        self.workspace_path.insert(0, "~/LocalVault")
        self.workspace_path.grid(row=1, column=0, sticky="ew", pady=(4, 12))

        ttk.Label(form, text="Passphrase", style="Glass.TLabel").grid(row=2, column=0, sticky="w")
        self.workspace_passphrase = tk.Entry(form, show="*")
        self.workspace_passphrase.grid(row=3, column=0, sticky="ew", pady=(4, 12))

        ttk.Label(form, text="Spaces (comma separated)", style="Glass.TLabel").grid(row=4, column=0, sticky="w")
        self.workspace_spaces = tk.Entry(form)
        self.workspace_spaces.insert(0, "personal, work")
        self.workspace_spaces.grid(row=5, column=0, sticky="ew", pady=(4, 12))

        form.columnconfigure(0, weight=1)

        ttk.Button(
            parent,
            text="Initialize Workspace",
            style="Glass.TButton",
            command=self._handle_init,
        ).pack(anchor="w", pady=(16, 0))

    def _build_encrypt_panel(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Encrypt & Decrypt", style="GlassTitle.TLabel").pack(anchor="w")

        ttk.Label(parent, text="Passphrase", style="Glass.TLabel").pack(anchor="w", pady=(12, 0))
        self.crypto_passphrase = tk.Entry(parent, show="*")
        self.crypto_passphrase.pack(fill="x", pady=(4, 12))

        ttk.Label(parent, text="Plaintext", style="Glass.TLabel").pack(anchor="w")
        self.plaintext = tk.Text(parent, height=6)
        self.plaintext.pack(fill="both", expand=True, pady=(4, 12))

        ttk.Button(
            parent,
            text="Encrypt →",
            style="Glass.TButton",
            command=self._handle_encrypt,
        ).pack(anchor="w")

        ttk.Label(parent, text="Encrypted Payload (base64)", style="Glass.TLabel").pack(anchor="w", pady=(16, 0))
        self.payload = tk.Text(parent, height=6)
        self.payload.pack(fill="both", expand=True, pady=(4, 12))

        ttk.Button(
            parent,
            text="Decrypt →",
            style="Glass.TButton",
            command=self._handle_decrypt,
        ).pack(anchor="w")

    def _handle_init(self) -> None:
        path = Path(self.workspace_path.get()).expanduser().resolve()
        passphrase = self.workspace_passphrase.get()
        spaces = [space.strip() for space in self.workspace_spaces.get().split(",") if space.strip()]

        if not passphrase:
            messagebox.showerror("Missing passphrase", "Please enter a passphrase.")
            return

        storage = EncryptedStorage(passphrase)
        workspace = Workspace(root=path, storage=storage)
        workspace.init_layout()
        workspace.write_metadata(spaces=spaces)
        salt_b64 = base64.b64encode(os.urandom(16)).decode("utf-8")
        workspace.write_keyinfo(KdfParams(), salt_b64)
        self._set_status(f"Workspace initialized at {path}")

    def _handle_encrypt(self) -> None:
        passphrase = self.crypto_passphrase.get()
        plaintext = self.plaintext.get("1.0", "end").strip()
        if not passphrase or not plaintext:
            messagebox.showerror("Missing data", "Provide a passphrase and plaintext.")
            return

        encrypted = encrypt_bytes(plaintext.encode("utf-8"), passphrase)
        encoded = base64.b64encode(encrypted).decode("utf-8")
        self.payload.delete("1.0", "end")
        self.payload.insert("1.0", encoded)
        self._set_status("Encryption complete.")

    def _handle_decrypt(self) -> None:
        passphrase = self.crypto_passphrase.get()
        payload = self.payload.get("1.0", "end").strip()
        if not passphrase or not payload:
            messagebox.showerror("Missing data", "Provide a passphrase and payload.")
            return

        try:
            raw = base64.b64decode(payload)
            plaintext = decrypt_bytes(raw, passphrase).decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Decrypt failed", str(exc))
            return

        self.plaintext.delete("1.0", "end")
        self.plaintext.insert("1.0", plaintext)
        self._set_status("Decryption complete.")

    def _set_status(self, message: str) -> None:
        self.status.configure(text=message)

    def run(self) -> None:
        self.root.mainloop()


def run_app() -> None:
    app = LocalVaultApp()
    app.run()
