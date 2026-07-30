---
title: "Write a Module"
description: "Add a Python-powered command to FlanLang without bloating the core."
order: 40
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.7"
---

# Write a module

Use a custom module when FlanLang needs a new ability that is not essential to every device. Keep it in `/programs/modules/` or the SD card’s `/modules/`, not `/os`.

## The smallest module

```py
def ping(ctx, text="pong"):
    return text


def get_module():
    return {
        "ping": ping
    }


def get_manifest():
    return {
        "name": "demo",
        "version": "1.0.0",
        "author": "You",
        "board": "any",
        "dependencies": [],
        "capabilities": []
    }
```

Save it as `demo.py`, reboot, then:

```fl
set reply to (demo ping "still alive")
log info reply
```

Every public action receives `ctx` first. Positional and named FlanLang arguments become normal Python arguments. Return small MicroPython-friendly values: strings, numbers, booleans, lists, dictionaries, or `None`.

## Manifest rules

- `name` is the FlanLang module name.
- `version` and `author` describe the package.
- `board` is `any`, `generic`, or the required board.
- `dependencies` lists module names that must load first.
- `capabilities` describes special provider roles.

Files beginning with `_` are private helpers and are skipped as public modules. This is useful for `_http.py` beside `fetch.py`.

## Tiny-device manners

- Import large libraries inside the action that needs them.
- Reuse buffers; do not keep duplicate file contents in RAM.
- Put program-specific state in `ctx.vars`, using a unique key.
- Add timeouts to network and hardware loops.
- Avoid writing unchanged values to flash.

Test the module on desktop when possible, then on real MicroPython. CPython saying “looks fine” is supportive, not legally binding.
