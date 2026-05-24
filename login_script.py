from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
from pathlib import Path
from compliance_scan import run_compliance_scan, select_filters, get_history, last_compare, go_to_compliance_scan, check_if_in_scan, download, select_history, search_controls
from finops import go_to_finsops, get_current_month, get_last_month, get_potential_yearly_savings, get_budget_status, get_savings_plan_data, get_recommendations_plan


def login(page, email, password):
    # Perform login
    page.fill("#emailAddress", email)
    page.fill("#password", password)
    page.get_by_role("button", name="Login").click()

    # Polling Logic
    target_path = "/home/overview"
    max_attempts = 30  # 30 seconds total
    logged_in = False

    for attempt in range(1, max_attempts + 1):
        current_url = page.url
            
        if target_path in current_url:
            print(f"Attempt {attempt}: Success! Reached {current_url}")
            logged_in = True
                # page.wait_for_timeout(3000)
            break
        else:
            print(f"Attempt {attempt}: Still at {current_url}. Waiting 1000ms...")
            page.wait_for_timeout(1000) # Playwright's version of sleep

    if not logged_in:
        print("Failed to reach target URL within 30 seconds.")

def login_with_polling(url, email, password):
    video_dir = Path.cwd() / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        # context = browser.new_context(record_video_dir=str(video_dir))
        context = browser.new_context()

        page = context.new_page()
        # page.pause()
        
        print(f"Navigating to {url}...")
        page.goto(url)

        login(page, email, password)
        select_filters(url, page, {"Severity": ["Critical"],
                                    "Status": ["Non-Compliant"]},
                                    frameworks=['CIS'])
        last_compare(url, page)
        download(url, page)
        # print(get_recommendations_plan(url, page))
        # total, avg = get_current_month(url, page)
        # percentage, total_change = get_last_month(url, page)
        # total_saving, saving_plan = get_potential_yearly_savings(url, page)
        # num, config_text = get_budget_status(url, page)
        # print(total, avg)
        # print(percentage, total_change)
        # print(total_saving, saving_plan)
        # print(num, config_text)
        # print(get_savings_plan_data(url, page))
        # search_controls(url, page, "Control")
        # page.wait_for_timeout(3000)
        # search_controls(url, page, "AWS")
        # page.wait_for_timeout(3000)
        # search_controls(url, page, "")
        # page.wait_for_timeout(5000)
        
        
        # context.close()
        # browser.close()
        # page.pause()


if __name__ == "__main__":
    # Replace with your actual credentials
    USER_EMAIL = "demotest02@gmail.com"
    USER_PASS = "5k3F?vE24^Ab!"
    LOGIN_URL = "https://demo.xops360.ai/" 
    
    login_with_polling(LOGIN_URL, USER_EMAIL, USER_PASS)