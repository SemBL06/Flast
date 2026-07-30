---
title: "Programs"
description: "Create, place, discover, and run FlanLang programs."
order: 13
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Programs

A program is a `.fl` file. For anything larger than a sneeze, give it a folder and call the entry file `main.fl`:

```text
party_sensor/
├── main.fl
├── data.yml
└── alarm.png
```

Put the folder in:

- `/programs/scripts/` for an internal program;
- `/scripts/` on the SD card for a removable program.

The default boot menu discovers both locations recursively. A folder named `party_sensor/main.fl` appears as **Party Sensor**.

## Smallest useful program

```fl
log info "The bean has booted"
display print "Hello!"
system sleep 1000
```

Upload the folder, reboot, and select it from the display menu. You can also launch a known path:

```fl
system run script="/programs/scripts/party_sensor/main.fl"
system run script="/sd/scripts/party_sensor/main.fl"
```

## Data and resources

Relative YAML and CSV files belong in the program folder. Use the storage commands instead of hardcoding the program’s full location:

```fl
data save file="data" path="launches" value=1
csv append file="events.csv" value=selected
```

`csv` must be installed as an optional module. See [Modules](modules.html), then continue with the [quickstart](../language/quickstart.html) or [syntax reference](../language/syntax.html).
