# CS2 Stat Scraper
***Disclaimer**: This tool is for educational and personal use only. It is not affiliated with or endorsed by csstats.gg. Please respect their [Terms of Service](https://csstats.gg/terms-of-use).*

<p align="center">
  <img src="images/icon-banner.png" alt="Example Image" width="300"/>
</p>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
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
[![Demo](images/demo-video-thumbnail.png)](https://youtu.be/M66f-juyNfk)


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
- ❗ Timeout Player data failed to load
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
