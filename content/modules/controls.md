---
title: "controls"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `controls`

`controls` is lower-level than `ui`. Use it when you want custom navigation, game-like input logic, or you’re building your own UI.

## Read a “clicked” direction

```fl
set clicked to (controls clicked)
if clicked == "left"
    log info "Left clicked"
end
```

## Check pressed state

```fl
if (controls pressed state=left)
    log info "Left is held down"
end
```

Convenience fields:

```fl
log info controls.left
log info controls.right
log info controls.up
log info controls.down
```
