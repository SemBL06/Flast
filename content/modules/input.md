---
title: "input"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `input`

`input` is the stable API for named sensors defined in `sd/main/main.yml`.

Example config:

```yml
input:
  tank_height:
    driver: ultrasonic
    trig: GP4
    echo: GP5
    height_cm: 120
```

Example script usage:

```fl
set distance_cm to (input get tank_height option=cm)
set water_height to (input get tank_height option=height)
```

Behind the scenes:

- `input` looks up your named device in config
- it finds the driver’s provider in `_capability_providers["input"]`
- it calls the provider’s `get(...)`
