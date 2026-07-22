---
title: "list"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `list`

Small list helpers to keep scripts readable.

```fl
set items to (list add items=[] value="hello")
set has_hello to (list contains items value="hello")
set first to (list get items index=0)
set n to (list length items)
set removed to (list remove items value="hello")
```

Available actions:

- `list add`
- `list remove`
- `list contains`
- `list get`
- `list length`
