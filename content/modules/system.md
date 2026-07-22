---
title: "system"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `system`

`system` provides “OS-ish” utilities: sleep, script discovery, cursor state, and running scripts.

## Sleep

```fl
system sleep 1000
```

## List scripts

Discovers scripts under `/sd/scripts` (recursive), returning a list of:

- `name`: human-friendly display name
- `path`: full path to the `.fl`
- `type`: `"script"`

```fl
set scripts to (system scripts)
log info "Found {scripts}"
```

You can also pass a custom path:

```fl
set scripts to (system scripts "/sd/scripts")
```

## Cursor helper

The UI stores the “current selection” as a cursor state. `system cursor` lets you read it.

```fl
set current to (system cursor position)
set index to (system cursor index)
```

## Run a script

Run the currently selected script from the menu:

```fl
system run selected
```

Or run an explicit file:

```fl
system run script="/sd/scripts/test/main.fl"
```

## Memory / GC (platform dependent)

```fl
set mem to (system memory)
set gc to (system gc)
log info mem
```
