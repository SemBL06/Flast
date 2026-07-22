---
title: "Runtime Architecture"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Runtime Architecture (Flan OS)

This runtime is built to stay **small, hackable, and MicroPython-friendly**: line-based parsing, lightweight instruction dictionaries, and a stable set of built-in script APIs.

## Big picture

1. **Parser** turns `.fl` source into instruction dictionaries.
2. **Executor** runs instructions (including loops and events).
3. **Modules** provide the script API (`display`, `ui`, `data`, …).
4. **Drivers / custom modules** plug into stable capabilities (`display`, `comm`, `input`, `output`).

## Core components

### Parser (`os/core/parser.py`)

Responsibilities:

- tokenize and parse line-based FlanLang
- emit instruction dictionaries:
  - `set`
  - `command`
  - `if` / `else`
  - `while`
  - `foreach`
  - `event`
  - `stop` / `skip`

### Executor (`os/core/executor.py`)

Responsibilities:

- value resolution (`( … )` expressions, variable lookup, interpolation)
- control flow execution (`if`, `while`, `foreach`)
- event registration + triggering
- module dispatch (`module action ...`)

Notable behavior:

- interpolation uses `{name}` placeholders and resolves variables + dotted paths
- `foreach i in 1-10` is treated as a numeric range
- `stop` and `skip` are implemented as loop-control exceptions

### Context (`os/core/context.py`)

Responsibilities:

- shared runtime state (`ctx.vars`)
- logging and exception reporting
- keeping track of current app/script paths (`ctx.app_path`, `ctx.data_path`)

## Modules (built-in script API)

Built-in modules are loaded from `os/modules/*` via `os/core/loaders/module_loader.py`.

Each module is registered by name (e.g. `display`, `ui`) and exposes a dict of callables returned by `get_module()`.

One fun detail: `display`, `log`, and `system` are separate script modules, but they share the same Python implementation file (`modules.system`) to keep the runtime footprint tiny.

## Drivers and capabilities

Drivers and installable modules can register providers into:

- `ctx.vars["_providers"]` (singleton providers, e.g. the active display)
- `ctx.vars["_capability_providers"]` (capability buckets, e.g. `comm`, `input`, `output`)

This is how hardware-specific code plugs into stable script APIs.

Next: [extensions/drivers.html](../extensions/drivers.html) and [extensions/custom-modules.html](../extensions/custom-modules.html).
