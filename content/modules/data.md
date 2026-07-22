---
title: "data"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `data`

`data` is the script-facing storage API. It reads/writes YAML and supports dot-path access into nested structures.

Two common file aliases:

- `file="main"`: `/sd/main/main.yml` (the main config)
- `file="data"`: the current script’s `data.yml` (`.../data.yml`)

## Read values: `data get`

```fl
set ssid to (data get file="main" path="wifi.SSID")
set height to (data get file="data" path="session.tank.height_cm")
```

Positional form is also supported:

```fl
set ssid to (data get "main" "wifi.SSID")
```

## Save values: `data save`

```fl
data save file="main" path="wifi.SSID" value="YourNetwork"
data save file="data" path="session.last_seen" value="today"
```

## Append to a list: `data append`

```fl
data append file="data" path="session.networks" value=selected.ssid
```
