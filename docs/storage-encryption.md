# Storage & Encryption

## Threat Model
- **Protect content at rest** on disk from casual inspection.
- **No plaintext files** should be written outside of memory.
- **Sync-safe**: encrypted files can be backed up or synced without exposing data.

## Encryption Model
- **Local-first**: all data encrypted on the user’s filesystem.
- **Per-workspace master key** derived from a user passphrase.
- **Per-file data keys** wrapped by the master key (envelope encryption).

## Suggested Scheme
- **KDF**: Argon2id for passphrase → master key.
- **AEAD**: XChaCha20-Poly1305 (fast, nonce-resistant) or AES-256-GCM.
- **Header**: store metadata (version, KDF params, wrapped file key).

### Encrypted File Layout (binary)
```
| magic | version | kdf params | wrapped file key | nonce | ciphertext |
```

## Read/Write Flow
1. User provides passphrase → derive master key.
2. For each file:
   - generate a random data key
   - encrypt file contents with data key (AEAD)
   - wrap data key with master key
3. Store header + ciphertext as a single `.enc` file.

## Indexing Strategy
- Decrypt content **only in memory** for building search/backlink indices.
- Persist indexes under `.vault/index/` **encrypted as well**.
- Cache derived data only if it can be fully rebuilt from encrypted sources.

## Backups & Sync
- User can sync the workspace directory via any tool (Git, Dropbox, rsync).
- Because files are encrypted, server-side access does not reveal plaintext.
- Optional: support separate device keys for multi-device unlock.

## Optional Enhancements
- Hardware-backed key storage (OS keychain / Secure Enclave).
- Split knowledge base into multiple vaults with separate keys.
- Per-space keys for compartmentalized security.
