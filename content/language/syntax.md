---
title: "FlanLang Syntax"
description: "The exact syntax understood by today’s FlanLang runtime."
order: 21
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# FlanLang syntax

This is the current language, not a dreamy “coming soon” specification.

## Values and variables

```fl
set count to 3
set name to "Pico"
set total to (math add count 4)
```

Integers are numbers. Double-quoted values are text. Unquoted words resolve to variables when one exists; otherwise they remain text.

Use dotted paths for items inside dictionaries and lists:

```fl
set first_name to scan.0.ssid
log info selected.path
```

Insert values into quoted text with braces:

```fl
log info "Hello {name}, total={total}"
```

## Commands and expressions

```fl
display print "Hi" x=center y=0
set length to (string length "banana")
```

A command is `module action`, followed by positional arguments, `name=value` arguments, or both. Parentheses turn a command into an expression whose result can be stored, compared, or passed elsewhere.

## Conditions

```fl
if temperature > 25 and fan == off
    log warn "It is becoming soup in here"
else
    log info "All chill"
end
```

Supported pieces:

- booleans: `on`, `off`;
- comparison: `==`, `is`, `!=`, `>`, `<`, `in`;
- logic: `and`, `or`, and a leading `not`;
- expressions: `if (button available)`.

Conditions evaluate from left to right. There are no grouping parentheses for boolean logic, so split complicated decisions into multiple `if` blocks.

## Loops

```fl
while on
    if (controls clicked) == "right"
        stop
    end
    system sleep 80
end
```

`stop` exits the current loop; `skip` jumps to its next round.

```fl
foreach item in items
    log info item
end

foreach number in 1-5
    log info number
end
```

Numeric ranges include both endpoints and may count down.

## Events

```fl
event system start
    log info "Started!"
end
```

`on system start` is also accepted. FlanOS triggers this event after the boot script executes.

## Comments

```fl
# The sensor is upside down because engineering happened
```

Comments occupy their own line and start with `#`. Inline comments are not supported.
