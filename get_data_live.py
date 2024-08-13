import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

SEASONS = list(range(2016, 2023))
DATA_DIR = "data" #creating directory
STANDINGS_DIR = os.path.join(DATA_DIR, "standings") #pointers to standings directory
SCORES_DIR = os.path.join(DATA_DIR, "scores")

def get_html(url, selector, sleep=5, retries=5):
    html = None
    for i in range(1, retries+1): # retry loop 
        time.sleep(sleep * i) # pauses program for 5 seconds, bypass fast scraping

        try:
            with sync_playwright() as p: # initializes pw instance
                browser = p.chromium.launch() # launches chromium browser
                page = browser.new_page()
                page.goto(url)
                print (page.title())
                html = page.inner_html(selector)
        except PlaywrightTimeout:
            print(f"Timeout error on {url}")
            continue # goes back to top of loop and tries again
        else: # runs if scrap is successful
            break
    return html # return none if fail, return html if success

def scrape_season(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = get_html(url, "#content .filter")

    soup = BeautifulSoup(html, features="html.parser")
    links = soup.find_all("a") #finds anchor tags
    href = [l["href"] for l in links]
    standings_pages = [f"https://basketball-reference.com{l}" for l in href]

    for url in standings_pages:
        save_path = os.path.join(STANDINGS_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = get_html(url, "#all_schedule")
        with open(save_path, "w+", encoding="utf-8") as f:
            f.write(html)

for season in SEASONS: # loop to scrape through each season
    scrape_season(season)

standings_files = os.listdir(STANDINGS_DIR)

def scrape_game(standings_file):
    with open(standings_file, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, features="html.parser")
    links = soup.find_all("a")
    hrefs = [l.get("href") for l in links]
    box_scores = [l for l in hrefs if l and "boxscore" in l and ".html" in l]
    box_scores = [f"https://www.basketball-reference.com{l}" for l in box_scores]

    for url in box_scores:
        save_path = os.path.join(SCORES_DIR, url.split("/") [-1])
        if os.path.exists(save_path):
            continue

        html = get_html(url, "#content")
        if not html:
            continue
        with open(save_path, "w+", encoding="utf-8") as f:
            f.write(html)

standings_files = [s for s in standings_files if ".html" in s] # filter dstore out

for f in standings_files:
    filepath = os.path.join(STANDINGS_DIR, f)
    
    scrape_game(filepath)