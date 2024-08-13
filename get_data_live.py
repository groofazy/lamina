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

season = 2016

url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"

html = get_html(url, "#content .filter")
