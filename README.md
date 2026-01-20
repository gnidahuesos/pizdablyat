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
- A **cross-platform desktop React app** shell (ready for Tauri/Electron packaging).

## Documents
- [Structure](docs/structure.md)
- [Filesystem Layout](docs/filesystem-layout.md)
- [Storage & Encryption](docs/storage-encryption.md)

## Quick Start (React Desktop Shell)
1. Install UI dependencies:
   ```bash
   cd ui
   npm install
   ```
2. Run the React shell:
   ```bash
   npm run dev
   ```
3. Open the local dev URL to view the desktop-style UI.
