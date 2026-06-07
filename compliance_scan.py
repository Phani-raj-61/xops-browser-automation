from pydantic import config
from playwright.sync_api import sync_playwright
from pathlib import Path
import config
import pickle

def go_to_compliance_scan(base_url, page):
    base_url = base_url.rstrip('/')
    target_url = f"{base_url}/secops/compliance"
    
    # 1. Check if we are already on the correct page
    if page.url != target_url:
        print(f"Navigating to {target_url}...")
        page.goto(target_url)
        # page.wait_for_timeout(10000)
        wait_for_page_load(page)
    else:
        print("Already on the target compliance page.")

def wait_for_page_load(page):
    # Find the div containing 'Score'
    while True:
        container = page.locator("div.absolute").filter(has_text="Score")
    
        # Get all spans in that div
        spans = container.locator("span").all()
        if len(spans) == 0 or spans[0].inner_text().strip() == '0%':
            print('Compliance page still loading. Waiting for 1000ms...')
            page.wait_for_timeout(1000)
            continue
    
        # If the text isn't 'Score' (case-insensitive), it must be our value
        print('Compliance page has succesfully loaded...')
            
        break

def check_if_in_scan(page):
    while True:
        button = page.get_by_role("button", name="Scan")
        if button.is_disabled():
            print("The scan is currently running. Waiting for 5000ms...")
            page.wait_for_timeout(5000)
            continue
        print("Scan is completed or did not run...")
        break

def search_controls(url, page, query):
    """
    Locates the control search box and enters a query.
    """
    # 1. Locate by placeholder
    go_to_compliance_scan(url, page)
    
    search_input = page.get_by_placeholder("Search controls...")
    
    # 2. Ensure it's ready
    search_input.wait_for(state="visible", timeout=5000)
    
    # 3. Clear and Type
    # fill() is better than type() because it handles clearing existing text automatically
    search_input.fill(query)
    
    # Optional: Press enter if the UI doesn't live-filter
    # search_input.press("Enter")
    
    print(f"Searching for: {query}")

def click_status_button_text_only(page, section_label, button_text):
    # This CSS selector translates to: 
    # 1. Find a paragraph that has the text <section_lavel>
    # 2. Find its sibling div immediately following it (+)
    # 3. Find the button inside that div
    selector = f"p:has-text('{section_label}') + div button:has-text('{button_text}')"
    
    try:
        target = page.locator(selector).first
        target.wait_for(state="visible", timeout=5000)
        target.click()
        print(f"Clicked {button_text} in the {section_label} section.")
    except Exception as e:
        print(f"Text-based lookup failed: {e}")

def get_history_dropdown_buttons(page):
    # 1. Locate the dropdown container (the absolute div)
    # Using the 'z-50' or 'top-full' classes helps identify the floating menu
    dropdown_container = page.locator("div.absolute.z-50")

    # 2. Find all buttons inside this dropdown
    # We use .all() to get a list of locators we can iterate over
    dropdown_buttons = dropdown_container.get_by_role("button").all()
    return dropdown_buttons

def extract_history_dates(page):
    """
    Extracts all dates and timestamps from the history dropdown.
    """
    history_data = []

    dropdown_buttons = get_history_dropdown_buttons(page)

    print(f"Found {len(dropdown_buttons)} history entries.")

    for button in dropdown_buttons:
        # Extract the primary text (the date)
        date_text = button.locator("span").inner_text()
        
        # Extract the secondary text (the timestamp)
        # Using the specific text-xs class helps isolate the time
        time_text = button.locator("div.text-xs").inner_text()
        
        history_data.append({
            "date": date_text.strip(),
            "timestamp": time_text.strip()
        })

    return history_data, dropdown_buttons

def get_history(base_url, page):
    """
    Locates the history container by its label and clicks the dynamic button beside it.
    """
    go_to_compliance_scan(base_url, page)
    if not config.SEC_OPS_HISTORY_CLICKED:
        config.SEC_OPS_HISTORY_CLICKED = True
        page.locator("div:has(> span:text('History')) + div button").click()
    return extract_history_dates(page)

def update_dates(base_url, page):
    history_data, _ = get_history(base_url, page)
    file_path = Path("sec_ops_dates.pkl")
    should_update = False
    if file_path.is_file():
        with open(file_path, "rb") as f:
            prev_data = pickle.load(f)
            if prev_data != history_data:
                should_update = True
    else:
        should_update = True
    if should_update:
        with open(file_path, "wb") as file:
            pickle.dump(history_data, file)
    return should_update


def select_history(base_url, page, idx = -1):
    # go_to_compliance_scan(base_url, page)
    # page.locator("div:has(> span:text('History')) + div button").click()
    if update_dates(base_url, page):
        print("In select history", config.SEC_OPS_HISTORY_CLICKED)
        return False
    date_buttons = get_history_dropdown_buttons(page)
    date_buttons[idx].click()
    config.SEC_OPS_HISTORY_CLICKED = False
    return True

def compare_dates(base_url, page, date1_idx, date2_idx):
    if update_dates(base_url, page):
        print("In select history", config.SEC_OPS_HISTORY_CLICKED)
        return False
    if date1_idx == date2_idx:
        print("Error: cannot perform date comparison.")
        return True
    select_history(base_url, page, date1_idx)
    compare_button = page.get_by_role("button", name="Compare")
    compare_button.click()

    vs_container = page.locator("div.border-blue-500\\/30").filter(
        has=page.get_by_text("vs.", exact=True)
    )

    target_button = vs_container.get_by_role("button")
    target_button.click()
    dropdown_container = vs_container.locator("div.absolute.z-50")
    dropdown_buttons = dropdown_container.get_by_role("button").all()
    if date2_idx < date1_idx:
        dropdown_buttons[date2_idx].click()
    else:
        print(date2_idx - 1)
        dropdown_buttons[date2_idx - 1].click()
    return True



    

def last_compare(base_url, page):
    go_to_compliance_scan(base_url, page)
    # page.pause()
    dates, date_buttons = get_history(base_url, page)
    date_buttons[-1].click()
    compare_button = page.get_by_role("button", name="Compare")
    compare_button.click()

    vs_container = page.locator("div.border-blue-500\\/30").filter(
        has=page.get_by_text("vs.", exact=True)
    )

    target_button = vs_container.get_by_role("button")
    target_button.click()

    dropdown_container = vs_container.locator("div.absolute.z-50")
    dropdown_buttons = dropdown_container.get_by_role("button").all()
    print(f"Found {len(dropdown_buttons)} history entries.")
    dropdown_buttons[-1].click()




def select_filters(base_url, page, filter_dict, frameworks="All"):
    go_to_compliance_scan(base_url, page)
    more_filters_button = page.get_by_role("button", name="More Filters")
    more_filters_button.click()
    clear_all_button = page.get_by_role("button", name="Clear All")
    clear_all_button.click()
    for status in filter_dict.keys():
        for filter_button_name in filter_dict[status]:
            
            click_status_button_text_only(page, status, filter_button_name)
    apply_filter_button = page.get_by_role("button", name="Apply Filters")
    apply_filter_button.click()
    if frameworks != "All":
        for framework in frameworks:
            button = page.get_by_role("button", name=framework)
            button.click()



def run_compliance_scan(base_url, page):
    """
    Handles navigation to SecOps, clicking Scan, and accepting Terms.
    Expects a Playwright 'page' object as input and 'base_url' of the webpage.
    """
    go_to_compliance_scan(base_url, page)
    
    scan_button = page.get_by_role("button", name="Scan")
    
    scan_button.wait_for(state="attached")
    scan_button.wait_for(state="visible")
    # Ensure it's ready to be clicked
    scan_button.wait_for(state="visible", timeout=10000)
    scan_button.click()

    print("Triggering Scan...")
    
    print("Waiting for Terms popup...")
    checkbox = page.locator("#isAgree")

    # We wait for the checkbox to be visible to ensure the popup is fully open
    checkbox.wait_for(state="visible", timeout=5000)
    checkbox.check()
    print("Checked '#isAgree'.")

    confirm_button = page.get_by_role("button", name="I Agree") 
    if confirm_button.is_visible():
        confirm_button.click()
        print("Scan confirmed.")
    check_if_in_scan(page)
    # page.wait_for_timeout(1000)
    # check_if_in_scan(page)

def download(base_url, page):
    go_to_compliance_scan(base_url, page)

    # 1. Define where you want to save the file
    download_dir = Path.cwd() / "downloads"
    download_dir.mkdir(exist_ok=True)

    # 2. Start waiting for the download event BEFORE clicking
    # This creates a context manager that catches the file as it streams
    with page.expect_download() as download_info:
        # Click your download button
        page.get_by_role("button", name="Download").click()
    
    # 3. Get the download object
    download = download_info.value
    
    # 4. Save it to your system
    # download.suggested_filename is the name the server intended (e.g., "report.pdf")
    file_path = download_dir / download.suggested_filename
    download.save_as(file_path)
    
    print(f"File successfully saved to: {file_path}")
    return str(file_path)
    # download_button = page.get_by_role("button", name="Download")
    # if download_button.is_visible():
    #     download_button.click()
    #     print("Report Downloading")

    
