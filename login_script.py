from playwright.sync_api import sync_playwright


def login(page, email, password):
    # Perform login
    page.fill("#emailAddress", email)
    page.fill("#password", password)
    button = page.get_by_role("button", name="Login")
    button.click()

    # Polling Logic
    target_path = "/home/overview"
    max_attempts = 30  # 30 seconds total
    logged_in = False
    while page.get_by_text("reCAPTCHA not ready. Please try again.", exact=True).count() > 0:
        print("Captcha Error Detected: Waiting 500ms before clicking...")
        button.click()
        page.wait_for_timeout(500)
        

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
