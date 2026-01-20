# Structure (Notion + Obsidian Hybrid)

## Core Concepts
- **Workspace**: top-level container of all content (like a vault).
- **Space**: optional grouping inside a workspace (e.g., Personal, Work).
- **Page**: main unit of content, stored as a Markdown file.
- **Block**: line- or paragraph-level unit with a stable ID (Notion-like blocks).
- **Database**: a special page that defines a schema and a collection of pages.
- **View**: a saved presentation of a database (table, kanban, calendar, list).
- **Template**: a reusable starter for pages or database rows.

## UX/Feature Mix
- **Notion-like**
  - Block-based editing with drag/drop and block IDs.
  - Inline databases (tables, kanban, calendar).
  - Page properties, templates, and relation/rollup fields.
- **Obsidian-like**
  - Local markdown files with frontmatter.
  - Graph view via backlinks and wiki-style links.
  - Extensible command palette and hotkeys.

## Page Format
A page is a Markdown file with frontmatter for metadata and a body for blocks.

```md
---
id: page-8d1b2
created: 2026-01-20T21:00:00Z
updated: 2026-01-20T21:45:00Z
space: personal
tags: [planning, roadmap]
properties:
  status: In Progress
  owner: "Alex"
---

# Project Roadmap

Intro paragraph. ^b-a1c2f

- [ ] Initial scope draft ^b-7f3a1
```

## Block IDs
Blocks are stored as Markdown with explicit IDs so they can be referenced.

```md
- [ ] Task item ^b-7f3a1
Some paragraph text. ^b-a1c2f
```

Stable block links reference these IDs:

```
[[Project Roadmap#^b-7f3a1]]
```

## Database Model
- A **database** is stored as a special page with a schema definition.
- Each **row** is a page file with properties and content.
- Views are derived from filters/sorts in the database metadata.

Example schema (YAML frontmatter in the database page):

```yaml
schema:
  status:
    type: select
    options: [Backlog, In Progress, Done]
  due:
    type: date
  owner:
    type: person
  effort:
    type: number
```

## Data Flow (High Level)
1. User edits a page in a block-based editor.
2. Editor persists to an encrypted Markdown file.
3. Indexer reads decrypted content (in-memory only) to build:
   - backlinks graph
   - search index
   - database views
4. UI renders pages from the local index.

## Linking Rules
- **Page links**: `[[Page Name]]`
- **Block links**: `[[Page Name#^block-id]]`
- **Embedded blocks**: `![[Page Name#^block-id]]`
