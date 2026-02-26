from playwright.sync_api import sync_playwright

def open_fiverr():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("Using existing Chrome session")

        page.goto("https://www.fiverr.com")

open_fiverr()
