from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_interactive_dom(url):
    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle")

        # JavaScript to find interactive elements
        # This looks for buttons, links, inputs, and anything with a 'pointer' cursor
        js_script = """
        () => {
            const interactives = [];
            const allElements = document.querySelectorAll('*');
            
            allElements.forEach((el) => {
                const style = window.getComputedStyle(el);
                const isButtonOrLink = ['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName);
                const hasPointer = style.cursor === 'pointer';
                const isVisible = el.offsetWidth > 0 && el.offsetHeight > 0;

                if ((isButtonOrLink || hasPointer) && isVisible) {
                    // We only keep essential attributes so the LLM doesn't get overwhelmed
                    interactives.push({
                        tagName: el.tagName,
                        id: el.id,
                        className: el.className,
                        text: el.innerText.trim().substring(0, 30),
                        type: el.getAttribute('type') || 'N/A'
                    });
                    
                    // Optional: Highlight them in the browser so you can see them
                    el.style.outline = '2px solid red';
                }
            });
            return interactives;
        }
        """
        
        print("Identifying interactive objects...")
        interactive_objects = page.evaluate(js_script)
        
        # Now get the cleaned DOM for context
        raw_html = page.content()
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # Strip the noise
        for tag in soup(["script", "style", "svg", "path", "footer", "nav"]):
            tag.extract()

        
        return {
            "interactives": interactive_objects,
            "cleaned_html": str(soup.body)
        }

if __name__ == "__main__":
    data = get_interactive_dom("https://demo.xops360.ai/")
    
    print(f"\nFound {len(data['interactives'])} interactive objects.")
    for obj in data['interactives']: # Print first 10
        print(f"- [{obj['tagName']}] Text: '{obj['text']}' | ID: {obj['id']}")