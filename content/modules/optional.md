---
title: "Optional Commands"
description: "What the example SD modules add, from Wi-Fi and HTTP to keyboards and tiny websites."
order: 33
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.7"
---

# Optional commands

The example `sdcard/modules/` folder is the toy cupboard. Copy only what your project needs.

| Module | Adds | Typical first call |
|---|---|---|
| `clock` | RTC/date and time helpers | `clock get` |
| `csv` | small table files | `csv append "log.csv" value` |
| `fetch` | HTTP client and listener | `fetch get url="http://..."` |
| `wifi` | Wi-Fi communication provider | `comm scan wifi seconds=2` |
| `bluetooth` | BLE communication provider | `comm scan bluetooth seconds=2` |
| `keyboard` | USB HID keyboard control | `keyboard print "hello"` |
| `mouse` | USB HID mouse control | `mouse move x=20 y=0` |
| `rfid` | RFID helper commands | `rfid contact` |
| `website` | tiny on-device HTTP website | `website start website="Website1"` |
| `demo` | extension test/example | `demo ping "hello"` |

## Communication providers

Wi-Fi and Bluetooth register under the stable `comm` API:

```fl
set providers to (comm list)
set networks to (comm scan wifi seconds=2)
set vendor to (comm get wifi vendor network=selected)
```

Provider-specific options vary. Wi-Fi credentials come from `/config/main.yml`.

## HTTP

```fl
set result to (fetch get url="http://example.com/data.json")
set code to (fetch status)
set value to (fetch response field="name")
fetch post url="http://example.com/score" value=score
```

`fetch listen` can accept simple incoming requests; see `sdcard/scripts/fetch_post_example/` for a working example.

## USB HID warning, because reality exists

Keyboard and mouse modules can control the connected computer when the board/firmware exposes HID support. Test with an empty text editor. Do not begin with “delete all my files.fl”.

Private helper files such as `_wifi_runtime.py` support public modules and are not called from FlanLang.
