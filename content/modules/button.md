---
title: "button"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `button`

`button` is the raw button backend accessor. Most scripts should prefer `controls` or `ui`, but `button` is great for diagnostics and compatibility.

## Common reads

```fl
set clicked to (button get clicked)
set left_down to (button get pressed state=left)
set left_raw to (button get raw state=left)
```

## Debug / availability

```fl
log info (button debug)
if (button available)
    log info "Button backend is active"
end
```

## Probe a pin (hardware debugging)

```fl
set result to (button probe pin=0)
log info result
```
