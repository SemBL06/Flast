---
title: "Where Files Live"
description: "The device and SD card layouts, and what belongs in each folder."
order: 12
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.8"
---

# Where files live

FlanOS keeps required files on the device and optional cargo on the SD card. No folder gets magically replaced by another folder wearing the same hat.

## Internal device

```text
/
├── main.py
├── os/                 essential runtime
├── config/
│   ├── main.yml        your hardware and secrets
│   └── boot.fl         startup menu
└── programs/
    ├── scripts/        internal programs + their data
    ├── modules/        optional internal commands
    └── drivers/        hardware needed without an SD card
```

## Optional SD card

```text
/
├── scripts/            removable programs + their data
├── modules/            optional commands, such as CSV
└── drivers/            hardware used with this card/setup
```

Internal drivers and modules load first. SD extensions are added afterward and cannot replace an internal extension unless `allow_override` is enabled. That default prevents a suspicious `math.py` on an SD card from becoming the new ruler of arithmetic.

## Where does program data go?

Beside the program:

```text
/scripts/plant_watcher/
├── main.fl
├── data.yml
└── readings.csv
```

FlanOS changes the active data folder while a program runs. `data.yml`, CSV files, websites, and other program resources can travel with the program folder.
