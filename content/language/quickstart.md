---
title: "FlanLang Quickstart"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# FlanLang Quickstart

FlanLang is a small line-based DSL designed to feel approachable on tiny devices.

## The three basics

### 1) Assign values with `set`

```fl
set name to "Sem"
set total to (math add 1 2)
```

### 2) Call commands as `module action ...`

```fl
display print "Hello!"
log info "Booted"
system sleep 250
```

### 3) Use expressions inside `( ... )`

Anything inside parentheses executes immediately and returns a value:

```fl
set scripts to (system scripts)
set selected to (ui options list=scripts field=name selected=0)
```

## Tiny example: show a menu, run selection

```fl
set scripts to (system scripts)
set selected to (ui options list=scripts field=name selected=0 right=continue)

while on
    set selected to (ui options right=continue)
    if (ui action) == "select"
        system run selected
        stop
    end
    system sleep 80
end
```

Next: [syntax.html](syntax.html) for the full set of control-flow shapes and value rules.
