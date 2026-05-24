import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from login_script import login
from compliance_scan import go_to_compliance_scan, select_filters, last_compare, download
from playwright.sync_api import sync_playwright

load_dotenv()

# Since the SSH tunnel is active, 'localhost' now maps to your AWS instance
openai_api_key = "empty"
openai_api_base = "http://localhost:8000/v1"
model_name = "Qwen/Qwen2.5-7B-Instruct-AWQ"

# print(openai_api_key)
content = 'You are tasked with returning the list of functions with proper input variables as per the query for browser automation. The output should be in the following format: <functions to call seperated by semicolons>'
content += Path('functions_info.txt').read_text() +'\n'
# print(content)


client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

url = "https://demo.xops360.ai/"
email = "demotest02@gmail.com"
password = "5k3F?vE24^Ab!"

print("Enter your prompt")
user_prompt = input()

# Chat completion
chat_response = client.chat.completions.create(
    # IMPORTANT: This must match the model string used in your vLLM Docker command
    model=model_name,
    messages=[
        {"role": "system", "content": content},
        {"role": "user", "content": user_prompt},
    ],
    # Optional: adjust temperature for more deterministic browser actions
    temperature=1.0 
)
print(chat_response.choices[0].message.content)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    print(f"Navigating to {url}...")
    page.goto(url)
    llm_output = chat_response.choices[0].message.content
    print(llm_output)
    for function in llm_output.split(';'):
        function = function.strip()
        if function == "":
            continue
        parts = function.strip().split('(', 1)
        if parts[0] == 'login':
            eval(parts[0] +'(page, email, password' + parts[1])
        elif parts[0] == 'select_filters' or parts[0] == 'search_controls':
            eval(parts[0] +'(url, page, ' + parts[1])
        else:
            eval(parts[0] +'(url, page' + parts[1])