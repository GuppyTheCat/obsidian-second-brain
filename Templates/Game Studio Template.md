---
categories:
  - "[[Companies]]"
type:
  - "[[Game studios]]"
---

## Games

```datacorejsx
const GamesView = await dc.require(dc.headerLink("Scripts/Views.md", "GamesView"));
return function View() { const studio = dc.useCurrentFile(); return <GamesView studio={studio} />; }
```
