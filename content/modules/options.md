---
title: "options"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `options` (Legacy-Compatible Menu Wrapper)

`options` is a compatibility wrapper over `ui options`. Prefer `ui options` for new scripts, but `options` is still handy for quick menus.

## Show (no input)

```fl
options show items=scripts field=name selected=0
```

## Interact (handles input)

```fl
set selected to (options interact items=scripts field=name selected=0)
```

Optional: run scripts on select:

```fl
set selected to (options interact items=scripts field=name selected=0 run=on)
```
