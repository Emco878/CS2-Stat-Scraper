# CS2 Stat Scraper
<p align="center">
  <img src="images/icon-banner.png" alt="Example Image" width="300"/>
</p>

[![forthebadge](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOTIuMDkzNzY1MjU4Nzg5MDYiIGhlaWdodD0iMzUiIHZpZXdCb3g9IjAgMCAxOTIuMDkzNzY1MjU4Nzg5MDYgMzUiPjxyZWN0IHdpZHRoPSIxMDMuNDg0MzgyNjI5Mzk0NTMiIGhlaWdodD0iMzUiIGZpbGw9IiNjYzAwMDAiLz48cmVjdCB4PSIxMDMuNDg0MzgyNjI5Mzk0NTMiIHdpZHRoPSI4OC42MDkzODI2MjkzOTQ1MyIgaGVpZ2h0PSIzNSIgZmlsbD0iI2IzMDAwMCIvPjx0ZXh0IHg9IjUxLjc0MjE5MTMxNDY5NzI2NiIgeT0iMjEuNSIgZm9udC1zaXplPSIxMiIgZm9udC1mYW1pbHk9IidSb2JvdG8nLCBzYW5zLXNlcmlmIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBsZXR0ZXItc3BhY2luZz0iMiI+TUFERSBXSVRIPC90ZXh0Pjx0ZXh0IHg9IjE0Ny43ODkwNzM5NDQwOTE4IiB5PSIyMS41IiBmb250LXNpemU9IjEyIiBmb250LWZhbWlseT0iJ01vbnRzZXJyYXQnLCBzYW5zLXNlcmlmIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iOTAwIiBsZXR0ZXItc3BhY2luZz0iMiI+UFlUSE9OPC90ZXh0Pjwvc3ZnPg==)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

![GitHub Created At](https://img.shields.io/github/created-at/Emco878/CS2-Stat-Scraper) 
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Emco878/CS2-Stat-Scraper/main)


# 📌 Description
**CS2 Stat Scraper** is a tool that processes multiple Steam profiles and retrieves their stats from `CSStats.gg`.

## 🛠️ Installation
Download `CS2 Stat Scraper.exe`

    ⚠️ Note: This app is unsigned - SmartScreen may warn you. It’s safe. The source code, can be found in `main.py`

## ✨ Features
- Input up to 10 Steam Profiles
- Score System
- Simple and easy-to-use interface

## 🎥 Demo


## 📊 Score System
The scoring system is simple: suspiciously high stats will be marked as 🟡 Yellow or 🔴 Red.

🔵 Blue = Average

🟡 Yellow = Higher than average

🔴 Red = Very unlikely to be legit

**KD**
```python
if winrate and hs >= 70:
    print("🔴 Not Legit")
    score += 2
elif winrate and hs >= 60:
    print("🟡 Higher than Average")
    score += 1
else:
    print("🔵 Average")
```

**HLTV Rating**
```python
if winrate and hs >= 1.5:
    print("🔴 Not Legit")
    score += 2
elif winrate and hs >= 1.3:
    print("🟡 Higher than Average")
    score += 1
else:
    print("🔵 Average")
```

**Win Rate and HS%**
```python
if winrate and hs >= 70:
    print("🔴 Not Legit")
    score += 2
elif winrate and hs >= 60:
    print("🟡 Higher than Average")
    score += 1
else:
    print("🔵 Average")
```

**ADR**
```python
if adr >= 110:
    print("🔴 Not Legit")
    score += 2
elif adr >= 100:
    print("🟡 Higher than Average")
    score += 1
else:
    print("🔵 Average")
```

## ⚠️ Fail-Safes
There are 4 possible error messages:
- ❗ Invalid Steam Profile Link
    - The link you entered is not in the correct format.
- ❗ This player has no match data
    - No data exists for that player on `CSStats.gg`.
- ❗ Could not resolve SteamID
    - The Steam profile does not exist.
- ❗ Timeout Player data filed to load
    - Not enough time to load data from `CSStats.gg`.
    - 💡 *Recommendation: Increase the Max Seconds per Instance (Max: 180)*

## 📦 Prerequisites
- Chrome
- Python 3.12 (Recommended)

## 👨‍💻 Development

Want to contribute? Great!

- Fork the repository: click the `Fork` button at the top-right of the page
- Your fork will be at: `https://github.com/your_username/CS2-Stat-Scraper`

Clone the repo using:

```bash
git clone https://github.com/your_username/CS2-Stat-Scraper.git
```
 🔗 For more help: [Contributing To a Project](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project).

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)
