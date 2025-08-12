import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def build_driver():
    """Create a Chrome WebDriver configured for headless CI usage."""
    opts = Options()
    # Run headless by default (override with HEADLESS=false)
    if os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}:
        opts.add_argument("--headless=new")
    # CI-friendly flags
    opts.add_argument("--no-sandbox")
    
    # opts.add_argument("--disable-dev-shm-usage")
    # opts.add_argument("--window-size=1366,768")
    # # fresh profile to avoid user-data-dir conflict
    # opts.add_argument(f"--user-data-dir={tempfile.mkdtemp(prefix='chrome-prof-')}")
    # opts.add_argument("--no-first-run")
    # opts.add_argument("--no-default-browser-check")
    return webdriver.Chrome(options=opts)