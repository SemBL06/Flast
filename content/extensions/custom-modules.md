---
title: "Custom Modules"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# Custom Modules (Installable Extensions)

Custom modules live under `sd/main/modules/*.py`.

They’re perfect for features that are:

- hardware-specific, or
- optional, or
- “nice to have” but not part of the minimal core

Some modules are **lazy-loaded**: they’re registered at boot and only imported when a script first uses them (see `LAZY_CUSTOM_MODULES` in `os/core/loaders/module_loader.py`).

## Minimal module shape

At minimum, a custom module should provide:

```py
def get_module():
    return {
        "ping": ping,
        "get": get,
    }
```

And then scripts can call it like:

```fl
demo ping "hello"
set status to demo.status
```

## Optional: manifest metadata

```py
def get_manifest():
    return {
        "name": "demo",
        "version": "1.0.0",
        "author": "You",
        "board": "any",
        "dependencies": [],
        "capabilities": [],
    }
```

Manifests are used for:

- update checks / metadata
- dependency + board filtering
- helping the runtime report what’s installed

## Provider-only modules

A module can be “provider-only” (no `get_module()`), used purely to register providers (display/comm/input/output). In that case, the manifest still matters so it can be tracked as installed.
