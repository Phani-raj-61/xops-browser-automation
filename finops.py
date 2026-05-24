from playwright.sync_api import sync_playwright

def go_to_finsops(base_url, page):
    base_url = base_url.rstrip('/')
    target_url = f"{base_url}/finops/overview"
    if page.url != target_url:
        print(f"Navigating to {target_url}...")
        page.goto(target_url)
        wait_till_page_load(page)
        # page.wait_for_timeout(10000)
        # target_element = page.get_by_text("Current Month", exact=True)
        # if target_element.count() == 0:
        #     print("Element does not exist.")
        #     return False
        # grandparent_element = target_element.locator("xpath=../..")
        # # print(grandparent_element.evaluate("el => el.outerHTML"))
        # print(grandparent_element.inner_text())
    else:
        print("Already on the target compliance page.")

def wait_till_page_load(page):
    prev_cost = -1
    while True:
        target_element = page.get_by_text("Current Month", exact=True)
        if target_element.count() == 0:
            print('Finops page still loading. Waiting for 1000ms...')
            page.wait_for_timeout(1000)
            continue
        grandparent_element = target_element.locator("xpath=../..")
        all_texts = grandparent_element.inner_text().splitlines()
        cost = all_texts[1]
        try:
            cost = float(cost.replace('$', '').replace(',', ''))
            if prev_cost != cost:
                print('Finops page still loading. Waiting for 500ms...')
                prev_cost = cost
                page.wait_for_timeout(500)
                continue
            print('Finops page has succesfully loaded...')
            break
        except ValueError:
            print('Finops page still loading. Waiting for 1000ms...')
            page.wait_for_timeout(1000)
            continue

def get_current_month(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("Current Month", exact=True).locator("xpath=../..")
    return target_element.inner_text().splitlines()[1:]

def get_last_month(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("vs Last Month", exact=True).locator("xpath=../..")
    return target_element.inner_text().splitlines()[1:]

def get_potential_yearly_savings(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("Potential Yearly Savings", exact=True).first.locator("xpath=../..")
    return target_element.inner_text().splitlines()[1:]

def get_budget_status(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("Budget Status", exact=True).locator("xpath=../..")
    return target_element.inner_text().splitlines()[1:]

def get_savings_plan_data(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("Savings Plan Overview", exact=True).locator("xpath=../../../../..")
    active_plans = target_element.get_by_text("Active Plans", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    coverage = target_element.get_by_text("Coverage", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    potential_yearly_savings = target_element.get_by_text("Potential Yearly Savings", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    total_commitment = target_element.get_by_text("Total Commitment", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    return active_plans, coverage, potential_yearly_savings, total_commitment

def get_recommendations_plan(base_url, page):
    go_to_finsops(base_url, page)
    target_element = page.get_by_text("Recommendation", exact=True).locator("xpath=../..")
    current_monthly_on_demnad_spend = target_element.get_by_text("Current Monthly On-Demand Spend", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    estimated_monthly_spend = target_element.get_by_text("Estimated Monthly Spend", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    estimated_monthly_savings = target_element.get_by_text("Estimated Monthly Savings", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    estimated_savings_percentage = target_element.get_by_text("Estimated Savings Percentage", exact=True).locator("xpath=..").inner_text().splitlines()[1]
    return current_monthly_on_demnad_spend, estimated_monthly_spend, estimated_monthly_savings, estimated_savings_percentage

    


