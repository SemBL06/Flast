---
title: "config"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `config` (Compatibility Wrapper)

`config` is a convenience wrapper around `data` that always targets the main config file (`file="main"`).

## Read

```fl
set ssid to (config get "wifi.SSID")
```

## Save

```fl
config save "wifi.SSID" "YourNetwork"
```

If you want the more explicit and flexible API, use `data` directly.
