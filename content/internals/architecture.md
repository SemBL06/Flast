---
title: "How FlanOS Works"
description: "A contributor’s map of boot, parsing, execution, modules, drivers, and storage."
order: 50
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.6"
---

# How FlanOS works

This page is for people who see a functioning gadget and immediately wonder which file they can poke.

## Boot

1. MicroPython runs `/main.py`.
2. `main.py` imports `/os/boot.py` without loading it as one enormous string.
3. Boot loads `/config/main.yml` and attempts the configured SD mount.
4. Built-ins register, mostly lazily.
5. Internal drivers/modules load before SD drivers/modules.
6. `/config/boot.fl` runs and usually shows the program menu.
7. The `system start` event fires.

No SD card is an ordinary state, not an emergency.

## Runtime pipeline

```text
.fl file
   ↓
Parser             one instruction dictionary per line
   ↓
Executor           variables, expressions, loops, events
   ↓
Module API         display, data, system, comm...
   ↓
Provider/driver    actual LCD, sensor, radio, or actuator
```

`core/parser.py` understands the line syntax. `core/executor.py` resolves values and dispatches commands. `Context` holds shared variables, active program paths, cached configuration, providers, and a bounded log history.

## Loading without eating all the RAM

Essential APIs live in `/os/modules/`. Optional Python lives under `/programs` or `/sd`. The loader validates manifests and dependencies, and can register selected modules by path without importing them until first use.

Internal extensions win name collisions by default. Enabling `allow_override` changes that rule, so treat it like hot sauce: deliberate amounts only.

## Storage

Configuration is cached in `Context` and saved only when changed. While a program runs, its folder temporarily becomes the active app/data path; afterward the previous paths are restored. That is why `file="data"` follows the program rather than a fixed global data directory.

## Contributor compass

- `/os/core/`: parser, executor, loaders, storage, utilities;
- `/os/modules/`: essential FlanLang APIs;
- `/programs/`: internal optional programs, modules, and drivers;
- `/config/`: device configuration and boot script;
- `sdcard/`: contents intended for an optional card;
- `selftest.py`: desktop integration and regression tests.

Keep the runtime simple enough for MicroPython. Clever is nice; having free RAM is nicer.
