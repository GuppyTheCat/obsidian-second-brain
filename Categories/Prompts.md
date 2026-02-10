---
tags:
  - categories
---

## Prompts

```datacorejsx
const { filterPagesByCategory, sortPages } = await dc.require(dc.headerLink("Scripts/Views.md", "PageUtils"));
return function View() {
  let pages = dc.useQuery("@page and linksto([[Prompts]])");
  pages = filterPagesByCategory(pages || [], "Prompts");
  pages = pages.filter(p => !(p.$path || "").includes("Templates/"));
  pages = sortPages(pages, p => p.value("created") || "", "desc");
  const COLUMNS = [
    { id: "Prompt", value: p => p.$link },
    { id: "Copy", value: p => <button type="button" onClick={() => { navigator.clipboard.writeText(p.value("prompt") || ""); if (typeof Notice !== "undefined") new Notice("Prompt copied to clipboard!"); }}>📋</button> },
    { id: "Topics", value: p => { const t = p.value("topics"); return t ? (Array.isArray(t) ? t.join(", ") : String(t)) : ""; }},
    { id: "Created", value: p => p.value("created") ? new Date(p.value("created")).toISOString().slice(0, 10) : "" }
  ];
  return <dc.Table columns={COLUMNS} rows={pages} />;
};
```

## Resources
![[Everything.base#Prompts - Resources]]