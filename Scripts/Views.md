# PageUtils

```datacorejs
function hasCategory(page, categoryName) {
  const cats = page.value ? page.value("categories") : page.categories;
  if (!Array.isArray(cats)) return false;
  return cats.some(c => {
    const p = c && (c.path || c.$path || (typeof c === "string" ? c : ""));
    return p && (p.endsWith(`${categoryName}.md`) || p.endsWith(categoryName));
  });
}
function pathToKey(path) {
  if (path == null || path === "") return "";
  const s = typeof path === "string" ? path : String(path);
  return s.split("/").pop().replace(/\.md$/i, "").trim();
}
function linkToKey(l) {
  if (!l) return "";
  const path = l.path || l.$path;
  if (path != null) return pathToKey(path);
  const str = typeof l === "string" ? l : String(l);
  const match = str.match(/\[\[([^\]|]+)/);
  return match ? match[1].trim() : pathToKey(str);
}
function containsCurrentFile(linkList, currentFilePath) {
  if (!linkList || currentFilePath == null) return false;
  const currentKey = pathToKey(currentFilePath);
  if (!currentKey) return false;
  const links = Array.isArray(linkList) ? linkList : [linkList];
  return links.some(l => linkToKey(l) === currentKey);
}
function isRelatedToCurrentFile(page, currentFile, relationFields = ["topics"]) {
  const currentFilePath = currentFile.$path || (currentFile.file && currentFile.file.path);
  for (const field of relationFields) {
    const val = page.value ? page.value(field) : page[field];
    if (containsCurrentFile(val, currentFilePath)) return true;
  }
  const aliases = currentFile.value ? currentFile.value("aliases") : currentFile.aliases;
  if (aliases && aliases.length > 0) {
    for (const field of relationFields) {
      const val = page.value ? page.value(field) : page[field];
      if (!val) continue;
      const arr = Array.isArray(val) ? val : [val];
      if (arr.some(t => {
        const name = t && (t.path || t.$path || String(t)).split("/").pop().replace(/\.md$/, "");
        return aliases.includes(name);
      })) return true;
    }
  }
  return false;
}
function filterPagesByCategory(pages, categoryName) {
  return pages.filter(p => hasCategory(p, categoryName));
}
function filterPagesByRelation(pages, currentFile, relationFields = ["topics"]) {
  return pages.filter(p => {
    if (!relationFields.some(f => p.value ? p.value(f) : p[f])) return false;
    return isRelatedToCurrentFile(p, currentFile, relationFields);
  });
}
function excludeTemplates(pages) {
  return pages.filter(p => !(p.$path || (p.file && p.file.path) || "").includes("Templates/"));
}
function sortPages(pages, sortBy, direction = "asc") {
  const out = [...pages];
  out.sort((a, b) => {
    let aVal = typeof sortBy === "function" ? sortBy(a) : (a.value ? a.value(sortBy) : a[sortBy]);
    let bVal = typeof sortBy === "function" ? sortBy(b) : (b.value ? b.value(sortBy) : b[sortBy]);
    if (direction === "desc") [aVal, bVal] = [bVal, aVal];
    if (aVal < bVal) return -1;
    if (aVal > bVal) return 1;
    return 0;
  });
  return out;
}
return { hasCategory, containsCurrentFile, isRelatedToCurrentFile, filterPagesByCategory, filterPagesByRelation, excludeTemplates, sortPages };
```

# DisplayUtils

```datacorejs
function formatRating(rating) {
  const m = { 7: "Безупречно", 6: "Отлично", 5: "Хорошо", 4: "Сносно", 3: "Плохо", 2: "Ужасно", 1: "Зло" };
  if (rating == null) return "-";
  return `${rating} - ${m[rating] || ""}`;
}
return { formatRating };
```

# MiranDailyNav

```datacorejsx
return function View() {
  const current = dc.useCurrentFile();
  const allPages = dc.useQuery("@page");
  const pattern = "Miran daily note";
  const filtered = dc.useMemo(() => {
    const lower = (pattern || "").toLowerCase();
    const list = (allPages || []).filter(p => (p.$name || "").toLowerCase().includes(lower));
    return list.sort((a, b) => ((a.$name || "").localeCompare(b.$name || "")));
  }, [allPages]);
  const currentIndex = (current && current.$name) ? filtered.findIndex(p => p.$name === current.$name) : -1;
  const links = [];
  if (currentIndex > 0) {
    const prev = filtered[currentIndex - 1];
    links.push(<a key="prev" data-href={(prev.$path || "") + (prev.$path && !prev.$path.endsWith(".md") ? ".md" : "")} className="internal-link">Previous</a>);
  }
  if (currentIndex >= 0 && currentIndex < filtered.length - 1) {
    const next = filtered[currentIndex + 1];
    links.push(<a key="next" data-href={(next.$path || "") + (next.$path && !next.$path.endsWith(".md") ? ".md" : "")} className="internal-link">Next</a>);
  }
  if (links.length === 0) return null;
  return <div style={{ marginTop: 0, marginBottom: 0, paddingTop: 0, paddingBottom: 0, fontSize: "0.9em" }}>{links.length === 2 ? <>{links[0]} | {links[1]}</> : links[0]}</div>;
}
```

# CopyPrompt

```datacorejsx
return function View() {
  const current = dc.useCurrentFile();
  const prompt = current && (current.value ? current.value("prompt") : current.prompt);
  if (!prompt) return null;
  const copy = () => {
    navigator.clipboard.writeText(prompt);
    if (typeof Notice !== "undefined") new Notice("Prompt copied to clipboard!");
  };
  return <button type="button" onClick={copy} style={{ marginBottom: "1em" }}>📋 Copy Prompt</button>;
}
```

# SoftwareView

```datacorejsx
const { filterPagesByCategory, filterPagesByRelation, sortPages } = await dc.require(dc.headerLink("Scripts/Views.md", "PageUtils"));
return function SoftwareView() {
  const currentFile = dc.useCurrentFile();
  let pages = dc.useQuery("@page and linksto([[Software]])");
  pages = filterPagesByCategory(pages || [], "Software");
  const pagesInCategory = pages || [];
  if (currentFile) {
    pages = filterPagesByRelation(pagesInCategory, currentFile, ["topics"]);
    if (pages.length === 0 && pagesInCategory.length > 0) {
      pages = pagesInCategory;
    }
  }
  pages = sortPages(pages || [], p => p.$name || "", "asc");
  const COLUMNS = [
    { id: "Name", value: p => p.$link },
    { id: "Description", value: p => p.value("description") || "" },
    { id: "URL", value: p => p.value("url") ? <a href={p.value("url")} rel="noopener">🔗</a> : "" },
    { id: "GitHub", value: p => p.value("github") ? <a href={p.value("github")} rel="noopener">🔗</a> : "" },
    { id: "Docs", value: p => {
      const d = p.value("docs");
      if (!d) return "";
      const arr = Array.isArray(d) ? d : [d];
      return <>{arr.map((url, i) => <a key={i} href={url} rel="noopener">📄 </a>)}</>;
    }},
    { id: "Platforms", value: p => p.value("platforms") || "" }
  ];
  return <dc.Table columns={COLUMNS} rows={pages} />;
};
```

# GamesView

```datacorejsx
const { hasCategory, sortPages } = await dc.require(dc.headerLink("Scripts/Views.md", "PageUtils"));
const { formatRating } = await dc.require(dc.headerLink("Scripts/Views.md", "DisplayUtils"));
return function GamesView({ studio }) {
  let pages = dc.useQuery("@page and linksto([[Games]])");
  pages = (pages || []).filter(p => {
    if (!hasCategory(p, "Games")) return false;
    if ((p.$path || "").includes("Templates/")) return false;
    if (studio) {
      const sp = studio.$path || (studio.path || "");
      const dev = p.value("developer");
      const pub = p.value("publisher");
      const devPath = dev && (dev.path || dev.$path);
      const pubPath = pub && (pub.path || pub.$path);
      return devPath === sp || pubPath === sp;
    }
    return true;
  });
  pages = sortPages(pages, p => p.value("title") || p.$name || "", "asc");
  const COLUMNS = [
    { id: "Cover", value: p => p.value("cover") ? <img src={p.value("cover")} alt="" style={{ maxWidth: 60, height: "auto" }} /> : "No Cover" },
    { id: "Name", value: p => p.$link },
    { id: "Status", value: p => p.value("status") || "-" },
    { id: "Rating", value: p => formatRating(p.value("rating")) },
    { id: "Platform", value: p => p.value("platforms") || "-" },
    { id: "Released", value: p => p.value("release_date") || "-" }
  ];
  return <dc.Table columns={COLUMNS} rows={pages} />;
};
```

# VideosView

```datacorejsx
const { filterPagesByRelation, sortPages } = await dc.require(dc.headerLink("Scripts/Views.md", "PageUtils"));
return function VideosView() {
  const currentFile = dc.useCurrentFile();
  let pages = dc.useQuery("@page and (linksto([[YouTube Videos]]) or linksto([[Videos]]))");
  pages = filterPagesByRelation(pages || [], currentFile, ["topics", "related"]);
  pages = sortPages(pages, p => p.value("published") || p.value("file")?.ctime || 0, "desc");
  const COLUMNS = [
    { id: "Video", value: p => p.$link },
    { id: "Channel", value: p => p.value("youtube_channel") || p.value("author") || "" },
    { id: "Duration", value: p => p.value("duration") || "" },
    { id: "Published", value: p => {
      const d = p.value("published");
      if (!d) return "";
      try { return new Date(d).toISOString().slice(0, 10); } catch { return String(d); }
    }},
    { id: "URL", value: p => p.value("url") ? <a href={p.value("url")} rel="noopener">🔗</a> : "" }
  ];
  return <dc.Table columns={COLUMNS} rows={pages} />;
};
```

# WebsitesView

```datacorejsx
const { filterPagesByCategory, filterPagesByRelation, sortPages } = await dc.require(dc.headerLink("Scripts/Views.md", "PageUtils"));
return function WebsitesView() {
  const currentFile = dc.useCurrentFile();
  let pages = dc.useQuery("@page and linksto([[Websites]])");
  pages = filterPagesByCategory(pages || [], "Websites");
  pages = filterPagesByRelation(pages, currentFile, ["topics"]);
  pages = sortPages(pages, p => p.$name || "", "asc");
  const COLUMNS = [
    { id: "Name", value: p => p.$link },
    { id: "Description", value: p => p.value("description") || "" },
    { id: "URL", value: p => p.value("url") ? <a href={p.value("url")} rel="noopener">🔗</a> : "" },
    { id: "Created", value: p => {
      const d = p.value("created");
      if (!d) return "";
      try { return new Date(d).toISOString().slice(0, 10); } catch { return String(d); }
    }},
    { id: "Topics", value: p => {
      const t = p.value("topics");
      return t ? (Array.isArray(t) ? t.join(", ") : String(t)) : "";
    }}
  ];
  return <dc.Table columns={COLUMNS} rows={pages} />;
};
```
