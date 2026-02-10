# Scripts

- **Script Organization:** Views and utilities are in `Scripts/Views.md` — shared Datacore view components and utilities (PageUtils, DisplayUtils, SoftwareView, GamesView, VideosView, WebsitesView, MiranDailyNav, CopyPrompt) under headings; load via `dc.require(dc.headerLink("Scripts/Views.md", "HeadingName"))`

- **Datacore usage:** When adding or editing dynamic views in notes:
  - Use ` ```datacorejsx` code blocks that return a React component: `return function View() { ... }`
  - Query data with `dc.useQuery("...")`, `dc.useCurrentFile()`, and optional `dc.useMemo()`
  - Render tables with `<dc.Table columns={COLUMNS} rows={pages} />` where columns are `{ id, value: page => ... }`
  - Share code via `dc.require(dc.headerLink("path/to/file.md", "SectionHeading"))`; the required block must return the component or helper object

- **View scripts:** To reuse a view in multiple notes, define it once under a heading in `Scripts/Views.md` and in each note use:
  - `const Component = await dc.require(dc.headerLink("Scripts/Views.md", "ComponentName")); return function View() { return <Component />; }`
  - Pass props (e.g. `studio`) when the view accepts them: `return <GamesView studio={dc.useCurrentFile()} />`

- **Refactoring:** When changing view or utility logic in `Scripts/Views.md`:
  - Notes that `dc.require` that section will pick up the change automatically
  - Ensure any new dependencies (e.g. PageUtils) are required at the top of the same code block
