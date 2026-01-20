# Notion + Obsidian (Encrypted Local Workspace)

This repository captures a **local-first knowledge system** that merges Notion’s structured blocks and databases with Obsidian’s Markdown files, backlinks, and graph navigation. All content is stored locally and **encrypted at rest**.

## Goals
- **Local-first** knowledge base with offline access.
- **Block-based editing** (Notion) on top of **Markdown-compatible files** (Obsidian).
- **Encrypted at rest** on the user’s filesystem.
- **Fast navigation** with backlinks, graph view, and full‑text search.
- **Future-proof files**: readable after decryption, independent of a single app.

## What’s Included
- A **structure spec** that defines the core content model (workspace → pages → blocks).
- A **filesystem layout** that describes how encrypted files live on disk.
- A **storage & encryption** design for local security.
- A **cross-platform desktop app** for macOS and Windows.

## Documents
- [Structure](docs/structure.md)
- [Filesystem Layout](docs/filesystem-layout.md)
- [Storage & Encryption](docs/storage-encryption.md)

## Quick Start (Desktop App)
1. Install the package requirements.
2. Run the desktop app:
   ```bash
   python -m localvault.cli app
   ```
3. Use the app to initialize a workspace and encrypt/decrypt text.
