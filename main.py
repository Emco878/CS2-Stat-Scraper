# MIT License
# Copyright (c) 2025 Andrew
# See LICENSE file for full license

# ---- GUI Customtkinter Imports ---- #
import customtkinter as ctk
import tkinter as tk

# ---- Regular Imports ---- #
# import sys, os
import requests, xml.etree.ElementTree as ET
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ---- Globals ---- #
steam_links = []

# ---- Resolve SteamID64 and Username from Steam Profile URL ---- #
def get_steam_id(url):
    if url.startswith("https://steamcommunity.com/"):
        xml_url = url.rstrip('/') + '?xml=1'  # Append ?xml=1 in the URL for XML format
        response = requests.get(xml_url, timeout=10)

        if response.status_code != 200 or not response.text.startswith("<?xml"):    # 'response.status_code != 200' catches network/server errors
            return None                                                             # 'not response.text.startswith("<?xml")' ensures Steam returned real XML, not an HTML error page
        
        try:
            root = ET.fromstring(response.text)  # ET.fromstring(...) now only runs on real XML, preventing crashes
            steam_id64 = root.find("steamID64").text
            username_text = root.find("steamID").text

            return steam_id64, username_text
        except Exception:
            return None

# ---- Selenium setup with Chrome logs suppressed ---- #
def make_driver():  # Build a quiet ChromeDriver
    chrome_opts = Options()
    chrome_opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_opts.add_argument("--log-level=3")   # Errors only
    service = Service(log_path="nul")   # “nul” discards ChromeDriver logs
    return webdriver.Chrome(service=service, options=chrome_opts)

# ---- GUI Setup ---- #
window = ctk.CTk()
window.geometry("550x885")
window.title("CS2 Stat Scraper")
window.configure(bg='#1E1E1E')
window.resizable(width=False, height=False)

# ---- Icon Setup ---- #
# def resource_path(relative_path):
#     # Supports PyInstaller and normal dev execution
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# window.iconbitmap(resource_path("icon.ico"))

# ---- Custom Time ---- #
def custom_time():
    value = max_seconds_input.get()
    if value.isdigit() and int(value) > 0 and int(value) <= 180:
        return int(value)
    elif value.isdigit() and int(value) > 180:
        return 180
    else:
        return 15

# ---- Steam Url ---- #
def steam_url():
    steam_link_input = steam_profile_link_input.get().strip()
    
    if steam_link_input.startswith("https://steamcommunity.com/"):
        if len(steam_links) < 10:
            steam_links.append(steam_link_input)
            steam_profile_error_label.configure(text="")
            shortened_steam_link = steam_link_input.split("/")[4]
            console_output.insert("end", f"Added: {shortened_steam_link}\n", "green_highlight")
            steam_profile_link_input.delete(0, "end")
        else:
            steam_profile_error_label.configure(text="Max 10 links allowed")
    else:
        steam_profile_error_label.configure(text="Invalid Steam Profile Link")
    console_output.see("end")

# ---- Keyboard ENTER Input ---- #
def enter_key_clicked(event=None):
        steam_url()

# ---- Main Scraping Logic ---- #
def generate_stats(driver, steam_id, username_text):
    driver.switch_to.new_window("tab")  # New tab
    driver.minimize_window()    # Minimizes the Window once a Chrome Instance Starts
    driver.get(f"https://csstats.gg/player/{steam_id}")
    
    try:
        WebDriverWait(driver, 2).until(   # Wait up to '2' seconds until the 'No matches have been added for this player' appears
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'No matches have been added for this player')]")
            )
        )

        #* NO DATA ACCOUNT STATUS *#
        console_output.insert("end", f"Steam Name: {username_text}\n")
        console_output.insert("end", "🔴 This player has no match data\n", "red_highlight")
        console_output.insert("end", "\n")
        console_output.see("end")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return

    except:
        try:
            WebDriverWait(driver, custom_time()).until(
                EC.presence_of_element_located((By.ID, "kpd"))
            )
        except:
            console_output.insert("end", f"🔴 Timeout: Player data failed to load for {username_text}\n\n", "red_highlight")
            console_output.see("end")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return

    doc = BeautifulSoup(driver.page_source, "html.parser")
    player_div = doc.find("div", id="player")
    if not player_div: return

    #* KD DIV *#
    kd = float(player_div.find("div", id="kpd").text.strip())

    #* HLTV_RATING DIV *#
    hltv_rating = float(player_div.find("div", id="rating").text.strip())

    #* STAT PANEL *#
    stat_panels = player_div.find_all("div", class_="stat-panel")  # Gets the stats of the Win Rate, HS, and ADR.
    win_rate = hs = adr = 0

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

    #* PRINT STATS *#
    score = 0
    def print_stats(value_red, value_yellow, label, tag, suffix="", decimal=True):
        nonlocal score
        if tag > value_red:
            highlight = "red_highlight"
            score += 2
        elif tag > value_yellow:
            highlight = "yellow_highlight"
            score += 1
        else:
            highlight = "lightblue_highlight"

        decimal_value = f"{tag:.2f}" if decimal else f"{int(tag)}"
        
        console_output.insert("end", f"{label}")
        console_output.insert("end", f"{decimal_value}{suffix}\n", highlight)
        return score

    #* USERNAME PRINT *#
    console_output.insert("end", f"Steam Name: {username_text}\n")

    #* KD PRINT *#
    score = print_stats(2.0, 1.6, "KD: ", kd)

    #* HLTV_RATING PRINT *#
    score = print_stats(1.5, 1.3, "HLTV Rating: ", hltv_rating)

    #* WIN RATE PRINT *#
    score = print_stats(70, 60, "Win Rate: ", win_rate, suffix="%", decimal=False)
    
    #* HS% PRINT *#
    score = print_stats(70, 60, "Headshot Percentage: ", hs, suffix="%", decimal=False)

    #* ADR PRINT *#
    score = print_stats(110, 100, "ADR: ", adr, decimal=False)

    #* SCORE PRINT *#
    if (score >= 9):
        console_output.insert("end", f"SCORE: {score}\n", "red_highlight")
    elif (score >= 7):
        console_output.insert("end", f"SCORE: {score}\n", "yellow_highlight")
    else:
        console_output.insert("end", f"SCORE: {score}\n", "lightblue_highlight")

    console_output.insert("end", "\n")
    console_output.see("end")
    
    driver.close()  # Close the stats tab
    driver.switch_to.window(driver.window_handles[0])  # Back to main tab

# ---- Start Button Command ---- #
def start_command():
    if not steam_links:
        steam_profile_error_label.configure(text="Invalid Steam Profile Link")
        console_output.see("end")
        return
    
    # Disable UI during scraping
    start_button.configure(state="disabled")
    enter_button.configure(state="disabled")
    clear_button.configure(state="disabled")
    steam_profile_link_input.configure(state="disabled")
    max_seconds_input.configure(state="disabled")

    # Start background thread
    threading.Thread(target=run_scraper, daemon=True).start()
    
    steam_profile_error_label.configure(text="")
    console_output.insert("end", f"\nUsing {custom_time()} seconds\n", "red_highlight")
    console_output.insert("end", "Loading...\n\n", "green_highlight")
    console_output.see("end")

    reset_gui()

# ---- Clear Button Command ---- #
clear_visible = False

def clear_confirm():
    global clear_visible
    if clear_visible:
        clear_yes.place_forget()
        clear_no.place_forget()
        clear_visible = False
    else:
        clear_yes.place(x=130, y=830)
        clear_no.place(x=30, y=830)
        clear_visible = True

def reset_gui():
    max_seconds_input.delete(0, "end")
    max_seconds_input.configure(placeholder_text="Default (15)")
    steam_profile_link_input.delete(0, "end")
    steam_profile_link_input.configure(placeholder_text="https://steamcommunity.com/")
    steam_profile_error_label.configure(text="")

def clear_command():
    reset_gui()
    console_output.delete("1.0", "end")
    steam_links.clear() # Clears Steam Links from memory

    console_output.insert("end", "🟢 Cleared\n\n", "green_highlight")

    # Hide Yes and No Button after Clearing
    clear_yes.place_forget()
    clear_no.place_forget()
    global clear_visible
    clear_visible = False

    console_output.after(500, lambda: console_output.delete("1.0", "end")) # After 1 second, call an anonymous function (lambda) that deletes all text from the textbox
    
# ---- Threading ---- #
def run_scraper():
    driver = make_driver()

    for url in steam_links:
        result = get_steam_id(url)
        if result:
            steam_id, username_text = result
            generate_stats(driver, steam_id, username_text)
        else:
            shortened_url = url.split("/")[4]
            console_output.insert("end", f"🔴 Could not resolve SteamID for: {shortened_url}\n", "red_highlight")
            console_output.see("end")

    driver.quit()
    steam_links.clear()

    # Re-enable UI after scraping
    start_button.configure(state="normal")
    enter_button.configure(state="normal")
    clear_button.configure(state="normal")
    steam_profile_link_input.configure(state="normal")
    max_seconds_input.configure(state="normal")
    
    console_output.insert("end", "🟢 All profiles processed!\n\n", "green_highlight")
    console_output.see("end")

#* TITLE *#
title_label = ctk.CTkLabel(window, text='CS2-Stat-Scraper', font=('Consolas', 56, 'bold'), text_color='#FFFFFF', fg_color="transparent", pady=20)
title_label.place(relx=0.5, y=0, anchor="n")

#* MAX SECONDS LABEL *#
max_seconds_label = ctk.CTkLabel(window, text='Max Seconds per Instance:', font=('Segoe UI', 18), text_color='#FFFFFF', fg_color="transparent")
max_seconds_label.place(x=30, y=100)

#* MAX SECONDS INPUT *#
max_seconds_input = ctk.CTkEntry(window, font=('Segoe UI', 18), width=240, height=38, corner_radius=8, fg_color="#1E1E1E", border_color="#FFFFFF", border_width=1.5,
                                 text_color="#FFFFFF", placeholder_text="Default (15)")
max_seconds_input.place(x=30, y=135)

#* STEAM PROFILE LINK LABEL *#
steam_profile_link_label = ctk.CTkLabel(window, text='Steam Profile Link:', font=('Segoe UI', 18), text_color='#FFFFFF', fg_color="transparent")
steam_profile_link_label.place(x=30, y=190)

#* STEAM PROFILE LINK INPUT *#
steam_profile_link_input = ctk.CTkEntry(window, font=('Segoe UI', 18), width=360, height=38, corner_radius=8, fg_color="#1E1E1E", border_color="#FFFFFF", border_width=1.5,
                                        text_color="#FFFFFF", placeholder_text="https://steamcommunity.com/")
steam_profile_link_input.place(x=30, y=225)
steam_profile_link_input.bind("<Return>", enter_key_clicked)    # Allows to press the ENTER Key on keyboard instead of the Button

#* STEAM PROFILE ERROR LABEL *#
steam_profile_error_label = ctk.CTkLabel(window, text="", font=('Segoe UI', 16), text_color='#FF0000', fg_color="transparent")
steam_profile_error_label.place(x=30, y=265)

#* CONSOLE TITLE LABEL *#
console_label = ctk.CTkLabel(window, text='Console:', font=('Segoe UI', 18), text_color='#FFFFFF', fg_color="transparent")
console_label.place(x=30, y=300)

#* CONSOLE OUTPUT *#
console_output = ctk.CTkTextbox(window, font=('Segoe UI', 16), width=480, height=480, corner_radius=8, fg_color="#1E1E1E", border_color="#FFFFFF", border_width=1.5,
                                text_color="#FFFFFF", wrap='none')
console_output.place(x=30, y=335)
console_output.bind("<Key>", lambda e: "break") # Block all keyboard input
console_output.configure(insertwidth=0) # Hide the cursor

console_output.tag_config("red_highlight", foreground="#FF0000")
console_output.tag_config("yellow_highlight", foreground="#FFFF00")
console_output.tag_config("lightblue_highlight", foreground="#00A6FF")
console_output.tag_config("green_highlight", foreground="#00FF00")

#* START BUTTON *#
start_button = ctk.CTkButton(window, command=start_command, text="START", font=('Segoe UI', 18), width=130, height=50, text_color='#FFFFFF', fg_color="transparent",
                             hover_color='#444444', border_color="#FFFFFF", border_width=1.5)
start_button.place(x=335, y=129)

#* ENTER BUTTON *#
enter_button = ctk.CTkButton(window, command=steam_url, text="Enter", font=('Segoe UI', 18), width=90, height=38, text_color='#FFFFFF', fg_color="transparent",
                             hover_color='#444444', border_color="#FFFFFF", border_width=1.5)
enter_button.place(x=420, y=225)

#* CLEAR BUTTON *#
clear_button = ctk.CTkButton(window, command=clear_confirm, text="Clear", font=('Segoe UI', 18), width=90, height=38, text_color='#FFFFFF', fg_color="transparent",
                             hover_color='#444444', border_color="#FFFFFF", border_width=1.5)
clear_button.place(x=30, y=830)

#* CLEAR YES *#
clear_yes = ctk.CTkButton(window, command=clear_command, text="Yes", font=('Segoe UI', 18), width=90, height=38, text_color='#FFFFFF', fg_color="transparent",
                             hover_color='#444444', border_color="#FFFFFF", border_width=1.5)

#* CLEAR NO *#
clear_no = ctk.CTkButton(window, command=clear_confirm, text="No", font=('Segoe UI', 18), width=90, height=38, text_color='#FFFFFF', fg_color="transparent",
                             hover_color='#444444', border_color="#FFFFFF", border_width=1.5)

# Bind to background clicks to remove focus
def unfocus(event):
    if isinstance(event.widget, (ctk.CTkEntry, ctk.CTkButton, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkSwitch, tk.Entry, tk.Button)): # If the clicked widget is an interactive input, don't remove focus
        return  # Keep focus
    window.focus()

window.bind("<Button-1>", unfocus)
window.mainloop()

# TODO: 