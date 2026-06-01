# Valorant Tracker

A Raspberry Pi stat tracker that scraped [Tracker.gg](https://tracker.gg/valorant) for Valorant competitive and unrated match statistics and displayed them on a 16x2 LCD screen. Built as a final project for CS 220 (Computer Architecture and Assembly Language) at CSUDH in May 2021.

> **Note:** This project no longer functions. Tracker.gg has changed their page structure since 2021, which breaks the string-index parsing used to extract stats. The code is preserved here as a reference.

---

## What it did

- Fetched the Tracker.gg player profile page using `urllib.request`
- Parsed win/loss/match stats for competitive and unrated game modes using positional string indexing and regex
- Displayed stats on an HD44780 16x2 i2c LCD connected to the Raspberry Pi GPIO
- Refreshed stats from the web every 3 minutes
- Cycled through game modes on the LCD display every 5 seconds

---

## Hardware

- **Raspberry Pi 4B** — Quad Core BCM2711, Cortex-A72, 1.5GHz, 4GB LPDDR4
- **HD44780 LCD** — 16x2 i2c character display connected via GPIO pins 2 (5V), 3 (SDA), 5 (SCL), 6 (GND)
- **PCF8574 GPIO expander** — I2C address `0x27` (fallback `0x3F`)

---

## Software

**Language:** Python 3  
**OS:** Raspberry Pi OS (Linux, kernel 5.10, 32-bit)

**Dependencies:**
- `urllib.request` — standard library, HTTP requests
- `re` — standard library, regex for stripping non-numeric characters
- `PCF8574` — GPIO expander driver (from FreeNove kit)
- `Adafruit_LCD1602` — LCD control library (from FreeNove kit)

No pip dependencies — the LCD libraries came bundled with the FreeNove Raspberry Pi kit.

---

## Configuration

In `valorant_tracker.py`, update the two `getOutputData()` calls with your Riot username and tagline:

```python
output = getOutputData("YourUsername", "NA1")
```

The user must have a public Tracker.gg profile linked to their Riot account.

---

## Why it broke

Tracker.gg has updated their page structure since 2021. The parser relied on hardcoded character offsets (e.g., `find_nth(output, "matchesPlayed", 0) + 125`) to locate stat values in the raw HTML string. Any change to the page layout shifts those offsets and breaks the output. A more robust implementation would use a proper HTML parser like `BeautifulSoup` or Tracker.gg's API if one becomes publicly available.

---

## Project writeup

Built for CS 220 at California State University, Dominguez Hills. The project writeup covers the hardware setup, LCD integration challenges, parsing approach, and planned improvements (button-based mode cycling, 3D printed case, handling accounts missing certain game modes).
