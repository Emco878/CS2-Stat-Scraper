# ---- Silence *all* stderr before noisy libraries load ---- #
import os, sys
sys.stderr.flush()
devnull = os.open(os.devnull, os.O_WRONLY)          # Windows “/dev/null”
os.dup2(devnull, 2)                                 # Redirect fd-2 (stderr)

# ---- Regular Imports ---- #
import time, requests, xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
init(autoreset=True) # Color reset after every print

# ---- Resolve SteamID64 from Steam Profile URL ---- #
def get_steam_id(url):
    xml_url = url.rstrip('/') + '?xml=1'  # Append ?xml=1 for XML format
    response = requests.get(xml_url, timeout=10)

    if response.status_code != 200:
        return None
    try:
        root = ET.fromstring(response.text)  # Parse XML
        steam_id64 = root.find("steamID64").text
        return steam_id64
    except Exception:
        raise Exception("SteamID64 not found.")

# ---- Selenium setup with Chrome logs suppressed ---- #
def make_driver():                                  # Build a quiet ChromeDriver
    chrome_opts = Options()
    chrome_opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_opts.add_argument("--log-level=3")       # Errors only
    service = Service(log_path="nul")               # “nul” discards ChromeDriver logs
    return webdriver.Chrome(service=service, options=chrome_opts)

# ---- Main Scraping Logic ---- #
def generate_stats(driver, steam_id):
    driver.switch_to.new_window("tab")  # New tab
    driver.get(f"https://csstats.gg/player/{steam_id}")
    time.sleep(5)

    doc = BeautifulSoup(driver.page_source, "html.parser")
    player_div = doc.find("div", id="player")
    if not player_div: return

    #* USERNAME *#
    username_text = player_div.find("div", id="player-info").text.strip()

    #* PRIVATE ACCOUNT STATUS*#
    if player_div.find("span", string="No matches have been added for this player"):
        print(f"\nSteam Name: {username_text}")
        print(f"{Fore.LIGHTBLACK_EX}This player has no match data or their profile is private.{Style.RESET_ALL}")
        return
        
    #* KD DIV *#
    kd = float(player_div.find("div", id="kpd").text.strip())

    #* HLTV_RATING DIV *#
    hltv_rating = float(player_div.find("div", id="rating").text.strip())

    stat_panels = player_div.find_all("div", class_="stat-panel")  # Gets the stats of the Win Rate, HS, and ADR.
    win_rate = hs = adr = 0

    score = 0

    #* STAT PANEL *#
    for panel in stat_panels:
        heading = panel.find("div", class_="stat-heading").text.strip()
        value_div = panel.find("div", style=lambda v: v and "font-size:34px" in v)
        if not value_div: continue
        value_text = value_div.text.strip().split()[0].replace("%", "")

        if "Win Rate" in heading:
            win_rate = int(value_text)
        elif "HS%" in heading:
            hs = int(value_text)
        elif "ADR" in heading:
            adr = int(value_text)

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

    #* HS% PRINT *#
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
        
    driver.close()  # Close the stats tab
    driver.switch_to.window(driver.window_handles[0])  # Back to main tab

# Main Program
if __name__ == "__main__":
    driver = make_driver()
    print("Enter up to 10 Steam Profile Links (Leave the input blank and press Enter to stop early):")
    
    steam_profiles = []
    while len(steam_profiles) < 10:
        print("Steam Profile Link >", end=" ", flush=True)  # Print the prompt without a newline, add a space after '>', and flush the output buffer immediately so it appears right away
        url = input().strip()                               # Wait for the user to type input, then remove any leading/trailing spaces or newlines

        if not url:
            break   # Stop early if input is blank

        steam_id = get_steam_id(url)
        if steam_id:
            steam_profiles.append(steam_id)
        else:
            print(f"{Fore.RED}Could not resolve SteamID for that link.{Style.RESET_ALL}")

    for steam_id in steam_profiles:
        generate_stats(driver, steam_id)
    
    driver.quit()   # Closes Chrome once the for loop is finished

    print("\nPress Enter to exit...", end=" ", flush=True)
    input()
    sys.exit()