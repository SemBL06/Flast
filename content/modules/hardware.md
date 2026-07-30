---
title: "Hardware & UI Commands"
description: "Cheat sheet for display, ui, controls, button, input, and output."
order: 31
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Hardware and UI commands

These commands stay the same while drivers handle the messy electrical details.

## `display`

```fl
if display available
    display clear
    display print "Hello" x=center y=0
    display invert
end
```

`display print` accepts text or a list. Coordinates may be numbers or helpers such as `center`, `left`, `right`, `top`, and `bottom`.

```fl
display effect type duration=80
display print "Typing..."
display shapes BOX text="OK" position=center
display image "/sd/scripts/app/logo.png" position=top_right
```

Effects are `type`, `blink`, `show`, `scroll`, or `none`. Image support depends on the active display driver.

## `ui`

Create and update a menu:

```fl
set programs to (system scripts)
set selected to (ui options list=programs field=name selected=0 right=continue)

while on
    set selected to (ui options right=continue)
    if (ui action) == "select"
        system run selected
        stop
    end
    system sleep 80
end
```

`ui action` returns `select`, `back`, or an empty value. `ui current` and `ui index` expose the current choice. Show scrollable text with:

```fl
ui description text=selected title="Details"
```

## `controls` and `button`

Use `controls` in normal programs:

```fl
set direction to (controls clicked)
if (controls pressed state=left)
    log info "Still holding left"
end
controls reset
```

Directions are `left`, `right`, `up`, and `down`. `controls available`, `controls raw`, `controls debug`, and `controls probe pin=0` are useful for diagnostics.

`button` exposes the raw backend with equivalent `get`, `available`, `debug`, and `probe` actions. It is mainly for debugging or compatibility; `controls` and `ui` are friendlier roommates.

## `input` and `output`

Named devices come from `/config/main.yml`:

```fl
set temperature to (input get room option=temperature)
output set lamp on
output set lamp pwm=128
set brightness to (output get lamp field=pwm)
```

Exact options depend on the configured driver. Your program uses the device name; the config chooses the driver and pins.

`options` and `description` still exist as compatibility wrappers, but new programs should use `ui`.
