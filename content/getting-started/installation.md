---
title: "Install FlanOS"
description: "Put MicroPython and FlanOS on a Raspberry Pi Pico W, with an optional SD card."
order: 11
sitemap:
  lastmod: "2026-07-30"
  changefreq: "monthly"
  priority: "0.9"
---

# Install FlanOS

You need a MicroPython board, a data-capable USB cable, and a computer. An SD card is optional. A cable that only charges is a very convincing liar.

## 1. Install MicroPython

For a Pico or Pico W:

1. Download the correct MicroPython UF2 from the [official Raspberry Pi guide](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
2. Unplug the Pico.
3. Hold **BOOTSEL** while plugging it in.
4. Release the button when the `RPI-RP2` drive appears.
5. Copy the UF2 onto that drive. The Pico reboots by itself.

Other boards have their own flashing ritual. Follow the board maker’s MicroPython instructions, then return here with heroic background music.

## 2. Connect with Thonny

Install [Thonny](https://thonny.org/), open it, then choose:

1. **Run → Configure interpreter**
2. Your MicroPython board as the interpreter
3. The correct USB/serial port
4. **View → Files**

You should now see your computer on top and the board below.

## 3. Upload the device files

Upload the **contents** of this repository’s `upload/` folder to the device root. When finished, the board should contain:

```text
/main.py
/os/
/config/
/programs/
```

Do not upload the outer `upload` folder itself. `/upload/main.py` will not boot; MicroPython looks for `/main.py`.

Copy `/config/main.example.yml` to `/config/main.yml`, then [configure your board](configuration.html). The real `main.yml` is ignored by Git because Wi-Fi passwords enjoy privacy too.

## 4. Add the optional SD card

Format the card as FAT and copy the **contents** of `sdcard/` to its root:

```text
/scripts/
/modules/
/drivers/
```

Insert it before booting. Default Pico W wiring is SCK GP18, MOSI GP19, MISO GP16, and CS GP17; change those values under `storage.sd` in `/config/main.yml` when your wiring differs.

## 5. Reboot

Press **Ctrl+D** in the MicroPython shell or reconnect power. Logs should appear in Thonny. No SD card? FlanOS continues with internal programs. No display? It logs that fact instead of dramatically fainting.

If boot fails, check that `main.py` is at the device root, `config/main.yml` is valid YAML, and your pin numbers match the wiring.
