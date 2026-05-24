import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI  # NIM uses the OpenAI client format
from langgraph.prebuilt import create_react_agent

# Load environment variables (NVIDIA_API_KEY, etc.) from a .env file
load_dotenv()

class BrowserAutomationSession:
    def __init__(self):
        # Keeps the browser context open across sequential tool interactions
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False) 
        self.page = self.browser.new_page()

    def get_tools(self):
        @tool
        def login(url: str, username: str, password: str) -> str:
            """
            Logs into the specified website using a username and password.
            Use this tool first when you need to authenticate into the system.
            """
            try:
                self.page.goto(url)
                # Replace these selectors with the specific targets from your layout
                self.page.fill('input[name="username"]', username)
                self.page.fill('input[name="password"]', password)
                self.page.click('button[type="submit"]')
                self.page.wait_for_load_state("networkidle")
                return f"Successfully logged into {url} as {username}."
            except Exception as e:
                return f"Failed to login: {str(e)}"

        @tool
        def go_to_compliance_scan() -> str:
            """
            Navigates the browser to the specific compliance scan sub-URL section.
            This tool should only be called AFTER a successful login.
            """
            try:
                compliance_url = f"{self.page.url.rstrip('/')}/compliance-scan"
                self.page.goto(compliance_url)
                self.page.wait_for_load_state("networkidle")
                return f"Successfully navigated to compliance section: {compliance_url}"
            except Exception as e:
                return f"Failed to navigate to compliance: {str(e)}"

        return [login, go_to_compliance_scan]

    def close(self):
        self.browser.close()
        self.playwright.stop()