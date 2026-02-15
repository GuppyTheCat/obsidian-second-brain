# Templater & Frontmatter

- **Date Format:** When creating or updating templates in the `Templates/` directory, always use the following Templater syntax for the `created` field in the frontmatter:
  ```yaml
  created: <%tp.date.now("YYYY-MM-DD")%>
  ```
  This ensures consistent ISO-like date formatting across all notes.

- **Frontmatter property order:** When creating or editing note frontmatter, use this order:
  - **Top (first, in order):** `categories` → `title` or `name` → `aliases` (if present).
  - **Middle:** Any other properties (order among them not specified).
  - **Bottom (last, in order):** `published` (if present) → `created` → `tags`.
- **Reordering all notes:** To update frontmatter property order across the whole vault (or a folder), use the **frontmatter-order** agent skill (`.cursor/skills/frontmatter-order/`): run its script with optional `--dry-run` or `--path`.