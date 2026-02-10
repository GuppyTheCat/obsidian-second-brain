# General Rules

- Always prioritize clarity and maintainability.
- **Query Priority:** Use Datacore for dynamic views. Write `datacorejsx` code blocks that return a React component; use `dc.useQuery()` for data and `<dc.Table />` or custom JSX for display. Put shared view logic in `Scripts/Views.md` under headings and load with `dc.require(dc.headerLink("Scripts/Views.md", "HeadingName"))`.