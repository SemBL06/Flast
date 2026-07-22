---
title: "Welcome"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Puddinator / Flan OS Docs

Welcome! This repo contains a tiny FlanLang runtime (the “OS”) plus a growing set of built-in modules, drivers, and installable extensions. The goal is simple: **write friendly scripts**, run them on small hardware, and keep the script APIs stable while the hardware layer evolves.

## Where to start

- New here? Start with:
  - [Overview](/getting-started/overview.html)
  - [quickstart](language/quickstart.html)
- Looking for a specific command? Jump to [modules](modules/).
- Hacking on the runtime itself? See [architecture(internals/architecture.html).
- Adding hardware or features? See [extensions](extensions/).

## Docs map

### Getting started

- [overview](getting-started/overview.html)
- [project-layout](getting-started/project-layout.html)

### FlanLang (the DSL)

- [Quickstart](language/quickstart.html)
- [syntax](language/syntax.html)

### Built-in modules (script API)

- [display](modules/display.html)
- [log](modules/log.html)
- [system](modules/system.html)
- [ui](modules/ui.html)
- [controls](modules/controls.html)
- [button](modules/button.html)
- [data](modules/data.html)
- [config](modules/config.html) (compat wrapper around `data file="main"`)
- [csv](modules/csv.html)
- [comm](modules/comm.html)
- [input](modules/input.html)
- [/output](modules/output.html)
- [list](modules/list.html)
- [math](modules/math.html)
- [string](modules/string.html)
- [options](modules/options.html) (legacy-compatible wrapper)
- [description](modules/description.html) (legacy-compatible wrapper)

### Runtime internals

- [architecture](internals/architecture.html)

### Extensions (drivers & custom modules)

- [drivers](extensions/drivers.html)
- [custom-modules](extensions/custom-modules.html)

(He wishes you a happy time)
![Test Image](assets/Monkey-Selfie.webp)
