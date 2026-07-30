---
title: "Start Here"
description: "A two-minute map of FlanOS, FlanLang, programs, modules, and drivers."
order: 10
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.9"
---

# Start here

FlanOS has four moving parts. Thankfully, none require a 600-page Java textbook.

| Part | What it does | Example |
|---|---|---|
| **FlanOS** | Boots the board and connects everything | Finds displays, programs, and optional storage |
| **FlanLang** | Runs your readable `.fl` files | `display print "Hello"` |
| **Modules** | Add commands | `math add`, `csv append`, `wifi scan` |
| **Drivers** | Talk to hardware | LCDs, OLEDs, sensors, SD cards |

Programs may live on the device or an SD card. The SD card is optional: remove it and internal programs still work. Program data stays beside its program, so copying one folder copies the whole tiny creature.

## Your first quest

1. [Install FlanOS](installation.html).
2. Learn [where files belong](storage-layout.html).
3. Follow the [FlanLang quickstart](../language/quickstart.html).
4. Put your creation on the board using [Programs](programs.html).

When something says “module” and something else says “driver,” do not panic. [Modules](modules.html) add abilities to the language; [drivers](drivers.html) make physical hardware behave.
