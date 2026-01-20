# Filesystem Layout

All user content lives under a single **workspace directory**. Files are encrypted at rest and only decrypted in memory for indexing/rendering.

```
workspace/
  .vault/
    vault.meta.json
    vault.keyinfo.json
    index/
      search.db.enc
      backlinks.db.enc
    cache/
      thumbs/
  spaces/
    personal/
      pages/
        welcome.md.enc
        daily-2026-01-20.md.enc
      databases/
        tasks.db.enc
        tasks/
          task-0001.md.enc
          task-0002.md.enc
    work/
      pages/
        roadmap.md.enc
  attachments/
    2026/
      01/
        diagram.png.enc
```

## Key Directories
- **.vault/**: internal metadata and encrypted index caches.
- **spaces/**: optional folders for logical separation.
- **pages/**: encrypted markdown pages.
- **databases/**: encrypted database files (schema + views).
- **databases/<db-name>/**: row pages for a database.
- **attachments/**: encrypted binary files.

## Naming Rules
- Each content file ends with `.enc` to indicate encrypted storage.
- The plaintext filename (e.g., `welcome.md`) is stored in the encrypted header.
- The encrypted filename can be either:
  - human-readable (for easy debugging), or
  - random IDs for extra privacy.

## Internal Metadata
`vault.meta.json` (encrypted) stores workspace-level metadata:

```json
{
  "workspaceId": "ws-91f1f",
  "created": "2026-01-20T21:00:00Z",
  "spaces": ["personal", "work"],
  "version": 1
}
```

`vault.keyinfo.json` stores **non-secret** parameters (KDF settings, salt, version).
