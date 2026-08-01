---
title: "Write a Driver"
description: "Connect new hardware to FlanOS display, controls, input, output, or communication capabilities."
order: 41
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.7"
---

# Write a driver

Drivers translate stable FlanLang commands into hardware behaviour. Programs should say `input get tank`; your driver handles pins, timing, and the sensor’s personal grudges.

Place drivers in internal `/programs/drivers/` or SD `/drivers/`.

## Choose a provider type

- **Display:** one active provider in `_providers`.
- **Controls:** one active provider in `_providers`, selected by `controls.driver`.
- **Input:** named sensors in the `input` capability.
- **Output:** named actuators in the `output` capability.
- **Comm:** multiple providers such as Wi-Fi and Bluetooth.

An input driver can expose:

```py
def get(ctx, name=None, config=None, positional=None, option=None, **kwargs):
    pin = config.get("pin")
    # Read hardware here.
    return 42


def get_input_provider(ctx):
    return {
        "get": get
    }
```

A controls provider can expose the shared button and joystick vocabulary:

```py
def get_controls_provider(ctx):
    return {
        "clicked": clicked,
        "pressed": pressed,
        "released": released,
        "value": value,
        "axis": axis,
        "available": available,
        "debug": debug,
        "reset": reset
    }
```

Add the same standard `get_manifest()` used by custom modules, with a capability such as `input`.

## Optional hooks

The loader recognises:

- `autoconfigure(ctx, config)` for safe, in-memory hardware detection;
- `get_display_provider(ctx)`;
- `get_controls_provider(ctx)`;
- `get_comm_provider(ctx)`;
- `get_input_provider(ctx)`;
- `get_output_provider(ctx)`;
- `get_module()` when the driver also exposes direct commands.

Autoconfiguration must fail safely. A missing sensor should not trap boot forever or rewrite the uploaded configuration with guesses.

## Driver checklist

1. Normalise pins such as `16` and `"GP16"`.
2. Bound every polling loop with a timeout.
3. Release buses or devices when an operation fails.
4. Log a useful error without dumping secrets.
5. Keep pure conversion/state logic testable without hardware.
6. Test the “device absent” path. Users are extremely talented at forgetting wires.

Study the included drivers in `upload/programs/drivers/` for complete manifests and provider shapes.
