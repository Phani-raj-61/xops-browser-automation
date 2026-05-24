from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def clean_and_extract(html_content):
    """
    Uses BeautifulSoup to strip away scripts, styles, and non-essential 
    elements to prepare the DOM for an LLM.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Remove tags that contain no useful 'knowledge' for an LLM
    for element in soup(["script", "style", "header", "footer", "nav", "aside", "noscript", "svg"]):
        element.extract()
    
    # 2. Get the cleaned text or cleaned HTML body
    # LLMs handle clean HTML well, but you could also use soup.get_text()
    cleaned_body = soup.find('body')
    
    if cleaned_body:
        # returns the HTML string of just the body, minus the junk tags
        return str(cleaned_body)
    return "No body content found."

def run_scraper(url):
    with sync_playwright() as p:
        # Launching visible browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        print(f"Opening: {url}")
        page.goto(url, wait_until="networkidle") # Waits for the network to be quiet
        
        # Get the full dynamic DOM
        raw_html = page.content()
        
        # Clean it with BeautifulSoup
        print("Cleaning DOM with BeautifulSoup...")
        final_context = clean_and_extract(raw_html)
        
        print("\n--- Processed Content for LLM ---")
        print(final_context)
        
        browser.close()
        return final_context

if __name__ == "__main__":
    target_url = "https://demo.xops360.ai/" 
    llm_ready_data = run_scraper(target_url)
    
    # Now you can send 'llm_ready_data' to your model