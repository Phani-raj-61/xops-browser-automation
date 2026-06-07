import os
import pickle
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from login_script import login
from compliance_scan import go_to_compliance_scan, select_filters, download, run_compliance_scan, select_history, compare_dates
from finops import go_to_finsops, get_current_month, get_last_month, get_potential_yearly_savings, get_budget_status, get_savings_plan_data, get_recommendations_plan
from cloudops import go_to_cloudops, run_cloudops_scan
from playwright.sync_api import sync_playwright
import config

load_dotenv()

# Since the SSH tunnel is active, 'localhost' now maps to your AWS instance
openai_api_key = "empty"
openai_api_base = "http://localhost:8000/v1"
model_name = "Qwen/Qwen2.5-7B-Instruct-AWQ"

def get_llm_response(content, user_prompt):
    chat_response = client.chat.completions.create(
    # IMPORTANT: This must match the model string used in your vLLM Docker command
    model=model_name,
    messages=[
        {"role": "system", "content": content},
        {"role": "user", "content": user_prompt},
    ],
    # Optional: adjust temperature for more deterministic browser actions
    temperature=0.0 
    )
    return chat_response.choices[0].message.content


def load_sec_ops_dates(pkl_path='sec_ops_dates.pkl'):
    if not Path(pkl_path).is_file():
        return "[]"
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    return ', '.join(f'"{item["date"].replace(",", "")} {item["timestamp"]}"' for item in data)

def get_system_content():
    content = 'You are tasked with returning the list of functions with proper input variables as per the query for browser automation. The output should be in the following format: <functions to call seperated by semicolons>'
    content += Path('functions_info.md').read_text() +'\n'
    content = content.replace('{{dates}}', load_sec_ops_dates())
    return content

# print(load_sec_ops_dates())


# print(openai_api_key)

# print(content)


client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

url = "https://demo.xops360.ai/"
email = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

print("Enter your prompt")
user_prompt = input()

parameterized_functions = ['select_filters', 'search_controls', 'select_history', 'compare_dates']
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    prev_skip = 0
    print(f"Navigating to {url}...")
    page.goto(url)
    while True:
        re_run = False
        llm_output = get_llm_response(get_system_content(), user_prompt).strip()
        curr_skip = 0
        print(llm_output)
        print(prev_skip)
        for i, function in enumerate(llm_output.split(';')):
            if i < prev_skip:
                continue
            function = function.strip()
            curr_skip += 1
            parts = function.strip().split('(', 1)
            if parts[0] == 'login':
                eval(parts[0] +'(page, email, password' + parts[1])
            elif parts[0] in parameterized_functions:
                if parts[0] == 'select_history' or parts[0] == 'compare_dates':
                    if not eval(parts[0] +'(url, page, ' + parts[1]):
                        prev_skip = curr_skip - 1
                        print('re run llm')
                        re_run = True
                        break
            else:
                eval(parts[0] +'(url, page' + parts[1])
        if not re_run:
            break