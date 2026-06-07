from playwright.sync_api import sync_playwright

def wait_for_page_load(page):
    while True:
        scan_button = page.get_by_role("button", name="Scan")
        if scan_button.count() > 0 and scan_button.is_visible() and scan_button.is_enabled():
            print("Cloudops Assests Management page has succesfully loaded...")
            break
        print("Cloudops Assests Management page still loading. Waiting for 500ms...")
        page.wait_for_timeout(500)

def go_to_cloudops(base_url, page):
    base_url = base_url.rstrip('/')
    target_url = f"{base_url}/cloudops/assestsManagement"
    if page.url != target_url:
        print(f"Navigating to {target_url}...")
        page.goto(target_url)
        wait_for_page_load(page)
    else:
        print("Already on the Cloudops Assests Management Page.")

def run_cloudops_scan(base_url, page):
    go_to_cloudops(base_url, page)
    scan_button = page.get_by_role("button", name="Scan")
    scan_button.click()
    scan_button = page.get_by_role("button", name="Scan")
    checkbox = page.locator("#isAgree")
    checkbox.wait_for(state="visible", timeout=5000)
    checkbox.check()
    confirm_button = page.get_by_role("button", name="I Agree") 
    confirm_button.click()
    print("Scan confirmed.")
    while scan_button.count() == 0 or not scan_button.is_visible() or not scan_button.is_enabled():
        print("Scan still running. Waiting for 5000ms...")
        page.wait_for_timeout(5000)
    print("Scan finished/ wasn't able to run.")