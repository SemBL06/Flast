---
title: "Project Layout (Mental Map)"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Project Layout (Mental Map)

Here’s the “what lives where” view you can keep in your head:

## Runtime

- `os/main.py`: boot flow (mount SD, load modules, run boot script).
- `os/core/*`: parser + executor + loaders + storage helpers.
- `os/modules/*`: built-in script modules (the stable API surface).

## SD image (what the runtime expects on-device)

- `sd/main/main.fl`: default boot script (launcher/menu).
- `sd/main/main.yml`: main configuration (storage, display, buttons, drivers/modules paths, etc.).
- `sd/main/drivers/*.py`: hardware drivers that can register providers (display/comm/input/output).
- `sd/main/modules/*.py`: installable extension modules (some are “lazy-loaded”).
- `sd/scripts/**/main.fl`: runnable scripts (discovered recursively).

Tip: the boot menu formats script names nicely (folder names become words), so `sd/scripts/ultrasonic_test/main.fl` shows up as “Ultrasonic Test”.
