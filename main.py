from selenium import webdriver
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
init()
import sys
import time

def generate_stats(steam_profiles):
    driver = webdriver.Chrome()
    driver.get(f"https://csstats.gg/player/{steam_id}")

    time.sleep(3)
    score = 0

    html = driver.page_source
    doc = BeautifulSoup(html, "html.parser")
    tags = doc.find_all("div", id="player")

    for tag in tags:
        #* USERNAME *#
        username_text = tag.find("div", id="player-info").text.strip()

        #* KD DIV *#
        kd_text = tag.find("div", id="kpd").text.strip()
        kd = float(kd_text)

        #* HLTV_RATING DIV *#
        hltv_rating_text = tag.find("div", id="rating").text.strip()
        hltv_rating = float(hltv_rating_text)


        stat_panels = tag.find_all("div", class_="stat-panel")  # Gets the stats of the Win Rate, HS, and ADR.

        #* WIN RATE DIV *#
        for panel in stat_panels:  # Loop through each stat panel
            heading = panel.find("div", class_="stat-heading")  # Look for the heading label inside the panel
            if heading and "Win Rate" in heading.text:  # Check if this panel is the Win Rate one
                styled_divs = panel.find_all("div", style=True)  # Get all divs with inline style (includes the 54% div)
                for div in styled_divs:  # Loop through those styled divs
                    if "font-size:34px" in div.get("style"):  # Look for the one with large font size (the 54% value)
                        win_rate_text = div.text.strip().replace('%', '').split()[0]  # Extract and clean the win rate text as well as replace the '%' with ''
                        win_rate = int(win_rate_text)
                        break  # Stop searching styled divs once found
                break  # Stop searching stat panels once Win Rate panel is found

        #* HS DIV *#
        for panel in stat_panels:
            heading = panel.find("div", class_="stat-heading")
            if heading and "HS%" in heading.text:
                styled_divs = panel.find_all("div", style=True)
                for div in styled_divs:
                    if "font-size:34px" in div.get("style"):
                        hs_text = div.text.strip().replace('%', '').split()[0]
                        hs = int(hs_text)
                        break
                break

        #* ADR DIV *#
        for panel in stat_panels:
            heading = panel.find("div", class_="stat-heading")
            if heading and "ADR" in heading.text:
                styled_divs = panel.find_all("div", style=True)
                for div in styled_divs:
                    if "font-size:34px" in div.get("style"):
                        adr_text = div.text.strip().split()[0] # .split()[0] cleans the text, splits it into words, takes the first word (the number)
                        adr = int(adr_text)
                        break
                break

        #* USERNAME PRINT *#
        print(f"\nSteam Name: {username_text}")

        #* KD PRINT *#
        if kd > 2.0:
            print(f"KD: {Fore.RED}{kd:.2f}{Style.RESET_ALL}")  # Red
            score += 2
        elif kd > 1.6:
            print(f"KD: {Fore.YELLOW}{kd:.2f}{Style.RESET_ALL}")  # Yellow
            score += 1
        else:
            print(f"KD: {Fore.LIGHTBLUE_EX}{kd:.2f}{Style.RESET_ALL}")  # Light Blue

        #* HLTV_RATING PRINT *#
        if hltv_rating > 1.5:
            print(f"HLTV RATING: {Fore.RED}{hltv_rating:.2f}{Style.RESET_ALL}")
            score += 2
        elif hltv_rating > 1.3:
            print(f"HLTV RATING: {Fore.YELLOW}{hltv_rating:.2f}{Style.RESET_ALL}")
            score += 1
        else:
            print(f"HLTV RATING: {Fore.LIGHTBLUE_EX}{hltv_rating:.2f}{Style.RESET_ALL}")

        #* WIN RATE PRINT *#
        if win_rate > 70:
            print(f"Win Rate: {Fore.RED}{win_rate}%{Style.RESET_ALL}")
            score += 2
        elif win_rate > 60:
            print(f"Win Rate: {Fore.YELLOW}{win_rate}%{Style.RESET_ALL}")
            score += 1
        else:
            print(f"Win Rate: {Fore.LIGHTBLUE_EX}{win_rate}%{Style.RESET_ALL}")

        #* HS PRINT *#
        if hs > 65:
            print(f"Headshot Percentage: {Fore.RED}{hs}%{Style.RESET_ALL}")
            score += 2
        elif hs > 50:
            print(f"Headshot Percentage: {Fore.YELLOW}{hs}%{Style.RESET_ALL}")
            score += 1
        else:
            print(f"Headshot Percentage: {Fore.LIGHTBLUE_EX}{hs}%{Style.RESET_ALL}")

        #* ADR PRINT *#
        if adr > 100:
            print(f"ADR: {Fore.RED}{adr}{Style.RESET_ALL}")
            score += 2
        elif hltv_rating > 45:
            print(f"ADR: {Fore.YELLOW}{adr}{Style.RESET_ALL}")
            score += 1
        else:
            print(f"ADR: {Fore.LIGHTBLUE_EX}{adr}{Style.RESET_ALL}")

        #* SCORE PRINT *#
        if score > 8:
            print(f"{Fore.RED}SCORE: {score}/10{Style.RESET_ALL}")
        elif score > 5:
            print(f"{Fore.YELLOW}SCORE: {score}/10{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTBLUE_EX}SCORE: {score}/10{Style.RESET_ALL}")

    driver.quit()

# Main Program
steam_profiles = []

while True:
    print("\nEnter up to 10 Steam Profile Links (Leave the input blank and press Enter to stop early):")
    while len(steam_profiles) < 10:
        url = input("Steam Profile Link > ").strip()

        if not url:
            break   # Stop early if input is blank
        elif url.lower() == "quit":
            sys.exit()

        parts = url.split("/")         # Split the URL by "/" so each section becomes a separate item in a list
        steam_id = ""                  # Create an empty variable to store the SteamID once we find it

        for part in parts:             # Go through each piece of the URL one by one
            if part.isdigit() and len(part) == 17:  # Check if this part is made only of digits and is exactly 17 characters long (SteamID64 is always 17 digits)
                steam_id = part        # If it's a valid SteamID, store it in the steam_id variable
                break
        
        if steam_id:
            steam_profiles.append(steam_id)
        else:
            print("Invalid Steam Profile Link")

    for steam_id in steam_profiles:
        generate_stats(steam_id)
    break

input("\nPress Enter to exit...")