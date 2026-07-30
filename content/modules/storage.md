---
title: "Storage Commands"
description: "Read and write configuration, YAML program data, and optional CSV files."
order: 32
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Storage commands

FlanOS keeps program data beside the running script. Moving the program folder therefore moves its memories too. Adorable.

## `data` — YAML with dotted paths

`file="data"` means the current program’s `data.yml`. `file="main"` or `file="config"` means `/config/main.yml`.

```fl
set launches to (data get file="data" path="stats.launches")
data save file="data" path="stats.launches" value=4
data append file="data" path="visitors" value=name
```

Short positional forms work too:

```fl
set ssid to (data get "main" "wifi.SSID")
```

Saving configuration writes to internal flash. Do it when a setting changes, not sixty times per second unless you dislike your flash chip.

## `config` — shorter configuration access

```fl
set ssid to (config get "wifi.SSID")
config save "wifi.SSID" "DefinitelyNotTheNeighbours"
```

This is a compatibility shortcut for `data` targeting the main config.

## `csv` — optional table storage

CSV is supplied in `/sd/modules/` and loads only when first used. Copy it to `/programs/modules/` if a no-SD program needs it.

```fl
csv append file="readings.csv" value=scan
set first to (csv get file="readings.csv" row=1)
set row to (csv get file="readings.csv" header="ssid" name="Cool-Wifi")
```

Rows are counted from 1. Relative filenames live beside the running program; absolute paths remain absolute.
