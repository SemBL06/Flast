---
title: "ui"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `ui`

`ui` is the high-level screen-flow layer: **menus** and **description pages**. It uses `display` for rendering and `controls`/`button` for navigation.

The `ui` module is designed so scripts stay readable and portable across hardware.

## Menu: `ui options`

Create a menu:

```fl
set selected to (ui options list=scripts field=name selected=0 right=continue)
```

Then keep it interactive by calling it again (no list needed):

```fl
while on
    set selected to (ui options right=continue)
    if (ui action) == "select"
        system run selected
        stop
    end
    system sleep 80
end
```

Navigation:

- `up` / `down`: move selection (wraps around)
- `left`: select
- `right`: returns `"back"` by default, or can be treated as “select” when `right=continue`

## Description page: `ui description`

```fl
ui description text=selected title="Details"
```

Behavior:

- wraps content across lines
- `up` / `down` scroll pages
- `right` returns `"back"`

## Read last action: `ui action`

After `ui options`, you can check what happened:

```fl
if (ui action) == "select"
    log info "User selected something!"
end
```

Action values:

- `"select"`
- `"back"`
- `""` (no meaningful action)
