---
title: "comm"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `comm`

`comm` is the stable communications capability API. Hardware-specific modules (like Wi‑Fi or Bluetooth) register themselves as `comm` providers.

## List installed comm providers

```fl
set providers to (comm list)
log info providers
```

## Scan

```fl
set networks to (comm scan wifi seconds=2)
```

## Get a value from an item

```fl
set vendor to (comm get wifi vendor network=selected)
```

Notes:

- Provider names are lowercase (e.g. `wifi`, `bluetooth`).
- The exact keyword arguments depend on the provider implementation.
