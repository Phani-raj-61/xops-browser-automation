# 🌐 xops-browser-automation

A modern, high-performance Python browser automation platform driven by LLM decision-making, managed seamlessly with `uv`.

---

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed on your host system:
* **Python 3.11 or higher**
* **uv** (Recommended) — Astral's lightning-fast Python package resolver.

### Install `uv` (Fastest Setup)
If you don't have `uv` installed yet, run the appropriate command for your system:

* **macOS / Linux:**
```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
```

* **Windows (PowerShell):**
```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🚀 Setup & Installation

Follow these step-by-step instructions to clone the repository, initialize your isolated environment, and fetch the required dependencies.

### Step 1: Clone the Repository
Open your terminal (or PowerShell on Windows) and run the following commands to pull the project code:

```bash
git clone [https://github.com/Phani-Raj-Goud/xops-browser-automation.git](https://github.com/Phani-Raj-Goud/xops-browser-automation.git)
cd xops-browser-automation
```

### Step 2: Create Environment & Sync Dependencies
With `uv`, you don't need to manually create virtual environment folders. The `sync` command reads the project configuration, automatically builds a local `.venv` folder, and installs all required packages deterministically:

```bash
uv sync
```

### Step 3: Create `.env` file to store `USER_NAME` and `PASSWORD` for site access
In order to login to the site using a specific user name and password create a new file named `.env` and write the following:
```bash
USER_NAME = <site_access_user_name>
PASSWORD = <site_access_password>
```

### Step 4: Install Browser Binaries (Playwright)
Because this is a browser automation project, you must download the necessary browser binaries (Chromium, Firefox, WebKit) inside your environment context before execution:

```bash
uv run playwright install
```

## 🏃 Execution Guide

The primary entry point for this automation workflow is `one_shot_llm.py`.

### Method 1: The Modern Way
The cleanest way to execute your code is via `uv run`. This securely targets your project's isolated environment dependencies without altering your terminal's shell state, meaning you don't have to deal with manually activating or deactivating environments:

* **Windows (PowerShell / CMD) & macOS / Linux:**
```bash
  uv run python one_shot_llm.py
```