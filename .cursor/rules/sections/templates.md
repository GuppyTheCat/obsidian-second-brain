# Templater & Frontmatter

- **Date Format:** When creating or updating templates in the `Templates/` directory, always use the following Templater syntax for the `created` field in the frontmatter:
  ```yaml
  created: <%tp.date.now("YYYY-MM-DD")%>
  ```
  This ensures consistent ISO-like date formatting across all notes.