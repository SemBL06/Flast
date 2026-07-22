---
title: "Drivers"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Drivers (Hardware Providers)

Drivers live under `sd/main/drivers/*.py` and are loaded at boot.

Drivers can do two things:

1. expose a module (optional) via `get_module()`
2. register providers for stable capabilities like `display`, `comm`, `input`, `output`

## Provider types

### Singleton providers (`_providers`)

Used when there should be one active implementation.

Example: `display` providers.

### Capability providers (`_capability_providers`)

Used when multiple backends can coexist, keyed by driver/module name.

Examples:

- `comm` providers: `wifi`, `bluetooth`, …
- `input` providers: `ultrasonic`, `dht11`, …
- `output` providers: (actuators, LEDs, relays, …)

## Typical driver hooks

Drivers may define some of these optional functions (see `os/core/loaders/module_loader.py`):

- `get_manifest()`: metadata (name/version/board/dependencies/capabilities)
- `get_config_defaults()`: default config values to merge into `main.yml`
- `autoconfigure(ctx, config)`: mutate config based on detected hardware
- `get_display_provider(ctx)`
- `get_comm_provider(ctx)`
- `get_input_provider(ctx)`
- `get_output_provider(ctx)`

If you’re writing a new driver, the easiest path is:

1. create `sd/main/drivers/your_driver.py`
2. return a provider dict from `get_*_provider(...)`
3. add a named device entry in `sd/main/main.yml` (for `input`/`output`) or a display config section
