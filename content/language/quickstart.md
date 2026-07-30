---
title: "FlanLang Quickstart"
description: "Learn enough FlanLang to make your board do something in ten minutes."
order: 20
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.9"
---

# FlanLang quickstart

FlanLang is line-based, small, and allergic to punctuation soup. Let’s build a tiny countdown.

## 1. Say things

Commands follow `module action arguments`:

```fl
log info "Preparing extremely important beeps"
display print "Ready?"
system sleep 500
```

Quotes keep text together. Numbers do not need quotes.

## 2. Remember things

```fl
set name to "Bean Machine"
set answer to (math add 40 2)
log info "{name} calculated {answer}"
```

`set` stores a value. Parentheses run a command and return its result. `{name}` inserts a value into quoted text.

## 3. Make decisions

```fl
if answer == 42
    display print "Correct. Obviously."
else
    display print "Math has escaped."
end
```

Blocks end with `end`; indentation is for humans and future-you.

## 4. Loop without summoning infinity

```fl
foreach number in 3-1
    display clear
    display print number
    system sleep 500
end

display print "Go!"
```

Ranges include both ends. `3-1` therefore produces `3`, `2`, `1`.

## 5. Save your masterpiece

Create `countdown/main.fl`, place the folder in internal `/programs/scripts/` or SD `/scripts/`, then reboot. The boot menu discovers it.

```fl
# countdown/main.fl
set title to "Tiny Rocket"
display print title

foreach number in 3-1
    display print number y=1
    system sleep 500
end

log info "Launch! (legally this is only an LED)"
```

Next, use the [syntax reference](syntax.html) when the language surprises you, and the [module cheat sheets](../modules/core.html) when you want the board to do more.
