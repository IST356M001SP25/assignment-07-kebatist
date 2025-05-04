# Tully's Good Times Menu Scraper
import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd
import os
from code.tully_scraper import tullyscraper
from playwright.sync_api import sync_playwright

def setup_module(module):
    # Run the scraper to generate the CSV file
    with sync_playwright() as playwright:
        tullyscraper(playwright)

def test_tullyscraper_menu_csv_file_exists():
    FILE = "code/cache/tullys_menu.csv"
    print(f"Expect {FILE} to exist!")
    assert os.path.exists(FILE)
def tullyscraper(playwright: Playwright) -> None:
    # Ensure the 'cache' directory exists
    os.makedirs("cache", exist_ok=True)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    extracted_items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_text = title.inner_text()
        print("MENU SECTION:", title_text) 
        row = title.query_selector("~ *").query_selector("~ *")
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            extracted_item = extract_menu_item(title_text, item_text)
            print(f"  MENU ITEM: {extracted_item.name}")
            extracted_items.append(extracted_item.to_dict())

    df = pd.DataFrame(extracted_items)
    df.to_csv("code/cache/tullys_menu.csv", index=False)    
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)

if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
    from menuitemextractor import extract_menu_item
    tullyscraper(playwright)

'''
import os
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item

def ensure_cache_directory():
    """Ensure the 'cache' directory exists."""
    os.makedirs("cache", exist_ok=True)

def scrape_menu_items(page):
    """Scrape menu items from the page and return a list of dictionaries."""
    extracted_items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_text = title.inner_text()
        print("MENU SECTION:", title_text)
        row = title.query_selector("~ *").query_selector("~ *")
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            extracted_item = extract_menu_item(title_text, item_text)
            print(f"  MENU ITEM: {extracted_item.name}")
            extracted_items.append(extracted_item.to_dict())
    return extracted_items

def save_to_csv(data, file_path):
    """Save the extracted data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def tullyscraper(playwright: Playwright) -> None:
    """Main scraper function to extract menu items and save them to a CSV file."""
    ensure_cache_directory()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Run the scraper to generate the CSV file
    with sync_playwright() as playwright:
        tullyscraper(playwright)'''