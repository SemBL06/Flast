---
title: "output"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `output`

`output` is the stable API for named actuators defined in `sd/main/main.yml`.

Example config:

```yml
output:
  led:
    driver: pwm_led
    pin: GP2
```

Example script usage:

```fl
output set led on
output set led pwm=128
set current to (output get led field="pwm")
```

Behind the scenes:

- `output set` calls the driver provider’s `set(...)`
- `output get` calls the driver provider’s `get(...)`
