---
name: frontmatter-order
description: Reorders YAML frontmatter properties in vault notes to match Second Brain conventions. Use when the user wants to update or normalize frontmatter order across all notes, or when asked to "reorder frontmatter" or "fix frontmatter order."
---

# Frontmatter Order

Reorders frontmatter in markdown notes so properties follow the vault's canonical order. See [Second Brain Rules](../../../Second%20Brain%20Rules.md) and [Templates rules](../../rules/sections/templates.md) for the convention.

## When to use

- User asks to update or fix frontmatter order in notes.
- User wants to apply the ordering rules to all notes (or a subset).

## Ordering rules

- **Top (first, in order):** `categories` → `title` or `name` → `aliases` (if present).
- **Middle:** Any other properties, alphabetically.
- **Bottom (last, in order):** `published` (if present) → `created` → `tags`.

## How to run

Run the script from the vault root. It processes all `.md` files under the vault that have frontmatter, excluding the `.cursor` directory.

```bash
python .cursor/skills/frontmatter-order/scripts/reorder_frontmatter.py
```

Optional: restrict to a path (e.g. one folder):

```bash
python .cursor/skills/frontmatter-order/scripts/reorder_frontmatter.py --path "Daily"
```

- **Dry run (no writes):** add `--dry-run` to print what would change without modifying files.
- **Requires:** Python 3.6+, PyYAML (`pip install pyyaml` or use `.cursor/skills/frontmatter-order/requirements.txt`).

## After running

- If the script reports errors (e.g. invalid YAML), fix those notes manually or adjust the script.
- Commit changes so the user can review the diff.
