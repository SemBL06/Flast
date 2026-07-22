---
title: "display"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `display`

The `display` module is the **main rendering API** for scripts. If a display provider is installed, it will draw to real hardware; otherwise, calls are safely ignored (and logged once).

## Common commands

### Print text: `display print`

```fl
display print "Hello"
display print "Top left" x=0 y=0
display print "Centered" x=center y=0
```

If you pass a list, each item is rendered on its own line.

### Clear / invert

```fl
display clear
display invert
```

### Effects: `display effect`

```fl
display effect type duration=80
display print "Typing vibe"
```

Effect types currently include: `type`, `blink`, `scroll`, `show`, and `none`.

### Simple shapes: `display shapes`

```fl
display shapes BOX text="Hello" x=center y=top
```

### Images: `display image`

```fl
display image image="/sd/scripts/app/Resources/logo.png" position=top_right
```

### Capability check: `display available`

```fl
if display available
    display print "Display detected!"
end
```
