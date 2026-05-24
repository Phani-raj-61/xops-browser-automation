from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_dom_visible(url):
    with sync_playwright() as p:
        # headless=False: Opens a physical browser window
        # slow_mo=1000: Delays actions by 1 second so you can follow along
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        page = browser.new_page()
        
        print(f"Navigating to {url}...")
        page.goto(url)
        
        # Taking a screenshot is a great way to verify what you're seeing
        page.screenshot(path="debug_view.png")
        
        # Get the DOM
        dom = page.content()
        
        print("DOM captured successfully.")
        
        # Keep the browser open for a few seconds if you want to inspect it manually
        # import time; time.sleep(5) 
        
        browser.close()
        return dom

def clean_dom(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Remove script and style elements
    for script_or_style in soup(["script", "style", "header", "footer", "nav", "noscript"]):
        script_or_style.extract()

    # Get text, but preserve some structure
    # You can also use soup.get_text() for pure text
    return str(soup.body) # Returns cleaned HTML body

if __name__ == "__main__":
    url_to_scrape = "https://demo.xops360.ai/"
    print(clean_dom(url_to_scrape))
    html_content = get_dom_visible(url_to_scrape)
    # print(html_content) # Uncomment to see the full HTML in your terminal