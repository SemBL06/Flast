---
title: "Drivers"
description: "Install hardware drivers and connect named devices through main.yml."
order: 15
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Drivers

A module adds a command. A driver persuades hardware to do something useful instead of sitting there looking electronic.

Drivers live in `/programs/drivers/` when they are required without an SD card, or `/drivers/` on the card when they belong to an optional setup. FlanOS loads them at boot.

Most programs should use stable APIs such as `display`, `input`, `output`, and `comm` instead of calling a driver directly. Your program asks for `input get greenhouse`; the config decides whether “greenhouse” is a DHT11, an ultrasonic sensor, or tomorrow’s ridiculous invention.

## Example: named sensor

In `/config/main.yml`:

```yml
input:
  tank:
    driver: "ultrasonic"
    trig: 4
    echo: 5
    height_cm: 120
```

In FlanLang:

```fl
set distance to (input get tank option=cm)
log info "Distance: {distance} cm"
```

## Installing a driver

1. Copy its `.py` file and `_helper.py` files into a driver folder.
2. Add its settings to `/config/main.yml`.
3. Reboot and watch the logs for its name.
4. Run a tiny hardware test before building the Death Star.

The included internal drivers cover LCD/OLED displays, DHT11, ultrasonic, PN532 NFC, and SD over SPI. Wiring and options differ per driver, so inspect its example config or source. Python authors can continue to [Writing drivers](../extensions/drivers.html).
