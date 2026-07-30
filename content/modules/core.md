---
title: "Core Commands"
description: "Cheat sheet for system, log, math, string, and list."
order: 30
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Core commands

These modules are built in and available on every FlanOS device.

## `system` — time, programs, and memory

```fl
system sleep 250
set programs to (system scripts)
system run selected
system run script="/sd/scripts/test/main.fl"
set memory to (system memory)
set collected to (system gc)
```

`system scripts` searches internal and mounted SD programs. Each result has `name`, `path`, and `type`. Pass a path to search only one folder.

The UI cursor can be read with `system cursor position`, `system cursor index`, or `system cursor marker`.

## `log` — talk to the serial console

```fl
log info "Normal news"
log warn "Suspicious news"
log error "Bad news"
log debug "Nerd news: {value}"
```

Only a configurable number of recent messages are kept in RAM; all messages still print as they happen.

## `math` — four heroic operations

```fl
set a to (math add 7 5)
set b to (math sub 7 5)
set c to (math mul 7 5)
set d to (math div 10 2)
```

Division by zero logs an error and returns no useful value, because even tiny computers have boundaries.

## `string` — text without drama

```fl
set message to (string concat "Hello " name)
set size to (string length message)
set loud to (string upper message)
set quiet to (string lower message)
```

## `list` — small collection helpers

```fl
set items to (list add items=items value="bean")
set found to (list contains items=items value="bean")
set first to (list get items=items index=0)
set size to (list length items)
set items to (list remove items=items value="bean")
```

Most actions return a new or updated value. Store the result when you want to keep it.
