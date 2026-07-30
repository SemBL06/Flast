---
title: "Modules"
description: "Understand built-in, internal, and SD modules without Python-induced fog."
order: 14
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Modules

Modules add words to FlanLang. In `math add 2 3`, `math` is the module and `add` is the action.

## Three flavours

| Kind | Location | Best for |
|---|---|---|
| Built-in | `/os/modules/` | Essential commands every device gets |
| Internal optional | `/programs/modules/` | Features needed without an SD card |
| SD optional | `/modules/` on the card | Large or rarely used features |

Do not put your own module in `/os`. Keeping the runtime boring and essential makes updates easier and boot memory smaller.

Optional modules are discovered at boot. Heavier ones can be lazy-loaded: FlanOS remembers their file but imports it only when a program first calls them. CSV lives on the example SD card for exactly this reason—not every blinking LED has spreadsheets.

## Installing one

Copy the module’s `.py` file and any private helper files beginning with `_` into an optional module folder. Reboot, then call it:

```fl
set reply to (demo ping "hello")
log info reply
```

Dependencies, board compatibility, and the public name come from its manifest. To create your own, visit [Writing custom modules](../extensions/modules.html). For available commands, use the [module cheat sheets](../modules/core.html).
