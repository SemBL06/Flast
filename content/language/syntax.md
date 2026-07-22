---
title: "FlanLang Syntax"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# FlanLang Syntax (What the Runtime Actually Understands)

This doc mirrors the current runtime behavior in `os/core/*` (not a “future spec”).

## Statements

### Assignment

```fl
set var_name to "text"
set total to (math add 1 2)
```

### Commands

```fl
module action
module action positional
module action key=value
module action positional key=value
```

## Values

### Strings + interpolation

```fl
set name to "Sem"
display print "Hello {name}"
```

Interpolation resolves:

- variables you `set`
- dotted paths into variables (e.g. `selected.name`)
- `module.field` lookups via `module get field` (when supported)

### Dot access

```fl
set first to scan.0.ssid
set status to demo.status
```

### Expressions

Expressions are just commands written in parentheses:

```fl
set total to (math add 1 2)
set chosen to (ui options list=scripts field=name)
```

## Control flow

### `if` / `else`

```fl
if condition
    log info "Yep"
else
    log warn "Nope"
end
```

### `while`

```fl
while on
    system sleep 100
end
```

Supported condition shapes include:

- `on` / `off`
- variables (truthy/falsey)
- comparisons: `==`, `!=`, `>`, `<`, `in`
- inline expressions: `if (controls pressed state=left) ... end`

### `foreach`

List iteration:

```fl
foreach wifi in scan
    log info wifi.ssid
end
```

Numeric range iteration:

```fl
foreach i in 1-10
    log info i
end
```

### Loop control: `stop` and `skip`

- `stop` breaks out of the current loop.
- `skip` continues to the next iteration of the current loop.

## Events

You can register event handlers:

```fl
event system start
    log info "System started!"
end
```

The runtime triggers `system start` after the boot script runs (see `os/main.py`).
