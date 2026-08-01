---
title: "Configure Your Board"
description: "Set storage pins, displays, controls, Wi-Fi, sensors, and actuators in main.yml."
order: 13
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Configure your board

Your device’s control panel is `/config/main.yml`. Start by copying `main.example.yml`; YAML rewards spaces and punishes tabs with mysterious sadness.

## SD card

```yml
storage:
  sd:
    driver: "sd_spi"
    slot: 0
    baudrate: 1000000
    path: "/sd"
    sck: 18
    mosi: 19
    miso: 16
    cs: 17
```

These Pico W defaults use SPI0. Pin values may be numbers or names such as `"GP16"`. FlanOS boots without a card if mounting fails.

## Display and controls

```yml
display:
  main:
    driver: "lcd_i2c"
    sda: 14
    scl: 15
    address: "auto"
    rows: 4
    cols: 20

controls:
  driver: "buttons"
  left: 0
  right: 1
  up: 2
  down: 3
  buttons_active_low: true
```

Change the driver and options to match your display. A missing display disables the menu but does not stop the OS.

## Wi-Fi

```yml
wifi:
  SSID: "YourNetwork"
  Password: "YourPassword"
```

Keep the real file private. Commit changes to `main.example.yml` when adding shareable settings, never your password unless you want the neighbours to become contributors.

## Named inputs and outputs

```yml
input:
  room:
    driver: "dht11"
    pin: 22

output:
```

The key (`room`) is the name used by FlanLang. The `driver` chooses the provider; remaining fields are passed to that driver.

`drivers.path` and `modules.path` normally remain `/programs/drivers` and `/programs/modules`. SD extensions are discovered separately after the card mounts.
