---
title: "Getting Started"
order: 0
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Getting Started

This project runs FlanLang scripts (files ending in `.fl`) using a lightweight Python/MicroPython-friendly runtime.

The “happy path” experience:

1. The OS boots from `/sd/main/main.fl`.
2. It scans `/sd/scripts` for scripts.
3. If a display + controls are available, you get a simple launcher menu.
4. Selecting an item runs that script.

If you’re mainly writing scripts, you’ll live in:

- `docs/language/*`
- `docs/modules/*`
- `sd/scripts/*` (example scripts)

If you’re extending hardware support, you’ll live in:

- `sd/main/drivers/*` (drivers/providers)
- `sd/main/modules/*` (installable extension modules)
