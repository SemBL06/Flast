---
title: "csv"
sitemap:
  lastmod: "2026-05-15"
  changefreq: "monthly"
  priority: "0.5"
---

# `csv`

`csv` is for simple “append rows, read back later” workflows. CSV files live next to your script (in the current script folder), unless you provide a full path.

## Append

```fl
csv append file="networks.csv" value=scan
```

Positional shorthand:

```fl
csv append "networks.csv" scan
```

## Read

Read by row number (1-based):

```fl
set first to (csv get file="networks.csv" row=1)
```

Read by `header` + `name`:

```fl
set row to (csv get file="networks.csv" header="ssid" name="Cool-Wifi")
```
