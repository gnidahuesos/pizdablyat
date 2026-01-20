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
- A **cross-platform UI** that runs locally in any modern browser on macOS and Windows.

## Documents
- [Structure](docs/structure.md)
- [Filesystem Layout](docs/filesystem-layout.md)
- [Storage & Encryption](docs/storage-encryption.md)

## Quick Start (Local UI)
1. Install the package requirements.
2. Run the local UI server:
   ```bash
   python -m localvault.server
   ```
3. Open `http://127.0.0.1:8000` in your browser to initialize a workspace and encrypt/decrypt text.
