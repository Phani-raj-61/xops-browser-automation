from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from login_script import login
from cloudops import go_to_cloudops, run_cloudops_scan
# from dashboard_extractor import extract_dashboard_data
from dotenv import load_dotenv
import os

load_dotenv()

def test(url, email, password):
    with sync_playwright() as p:
        # headless=False: Opens a physical browser window
        # slow_mo=1000: Delays actions by 1 second so you can follow along
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        page = browser.new_page()
        
        print(f"Navigating to {url}...")
        page.goto(url)
        login(page, email, password)
        go_to_cloudops(url, page)
        run_cloudops_scan(url, page)
        # page.wait_for_timeout(20000)
        # print(extract_dashboard_data(page))
        # go_to_compliance_scan(url, page)
        # click_scan_and_wait(page)
        # should_update, dates, dropdown_buttons = update_dates(url, page)
        # print(should_update)
        # print(dates)
        
        
        # Keep the browser open for a few seconds if you want to inspect it manually
        # import time; time.sleep(5) 
        
        browser.close()

if __name__ == "__main__":
    LOGIN_URL = "https://demo.xops360.ai/"
    test(LOGIN_URL, os.getenv('USER_NAME'), os.getenv('PASSWORD'))
    # print(html_content) # Uncomment to see the full HTML in your terminal