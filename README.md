# CS2 Stat Scraper
***Disclaimer**: This tool is intended for personal and educational use only. It is not affiliated with or endorsed by csstats.gg.  
Any commercial use of this software, directly or indirectly, is against csstats.gg’s [Terms of Service](https://csstats.gg/terms-of-use) and is strictly prohibited.*


<p align="center">
  <img src="images/icon-banner.png" alt="Example Image" width="300"/>
</p>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

![GitHub Created At](https://img.shields.io/github/created-at/Emco878/CS2-Stat-Scraper) 
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Emco878/CS2-Stat-Scraper/main)
[![GitHub release](https://img.shields.io/github/v/release/Emco878/CS2-Stat-Scraper?label=latest%20release)](https://github.com/Emco878/CS2-Stat-Scraper/releases/latest)



# 📌 Description
**CS2 Stat Scraper** is a tool that processes multiple Steam profiles and retrieves their stats from `CSStats.gg`.

## 🛠️ Installation
Download the latest release version of [CS2 Stat Scraper.exe](https://github.com/Emco878/CS2-Stat-Scraper/releases/latest)

>⚠️ Note: This app is now signed however SmartScreen may warn you as my repuration is low. The program is safe. The source code, can be found in `main.py`

## ✨ Features
- Input up to 10 Steam Profiles
- Score System
- Simple and easy-to-use interface

## 🎥 Demo
[![Demo](images/demo-video-thumbnail.png)](https://youtu.be/M66f-juyNfk)


## 📊 Score System

> ⚠️ *Note: These are examples of the logic. This is not actual code from `main.py`.*

The scoring system is simple: *Average High Stats* are marked as 🟡 Yellow, while *Suspiciously High Stats* are marked as 🔴 Red.

🔵 **Blue** = Average  
🟡 **Yellow** = Higher than average  
🔴 **Red** = Very unlikely to be legit

**The score is out of 10**  
A score between **0-6** will return a 🔵 *Average Account.*  
A score between **7–8** will return a 🟡 *Suspiciously High Account.*  
A score between **9–10** will return a 🔴 *Likely Cheating Account.*

**KD**
```python
if kd >= 2.0:
    print("🔴 Not Legit")
    score += 2
elif kd >= 1.6:
    print("🟡 Higher than Average")
    score += 1
else:
    print("🔵 Average")
```

**HLTV Rating**
```python
if hltv_rating >= 1.5:
    print("🔴 Not Legit")
    score += 2
elif hltv_rating >= 1.3:
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

## 📦 Requirements
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