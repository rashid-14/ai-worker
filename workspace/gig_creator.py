import time
from playwright.sync_api import sync_playwright

def create_gig():
    with sync_playwright() as p:
        print("Connecting to Fiverr...")

        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("Connected to Fiverr page")

        # Step 1 - Ensure Fiverr Home
        page.goto("https://www.fiverr.com/")
        time.sleep(5)

        # Step 2 - Try switch to selling (if needed)
        try:
            page.locator("text=Switch to Selling").click(timeout=4000)
            print("Switched to Selling Mode")
            time.sleep(5)
        except:
            print("Already in Selling Mode")

        # Step 3 - Open Gig Creation Page
        print("Opening Gig Creation Page...")
        page.goto("https://www.fiverr.com/manage_gigs/create")
        time.sleep(5)

        # 🚨 HUMAN CHECKPOINT
        print("\n⚠️ Fiverr may show PRESS & HOLD verification")
        input("👉 Complete it manually in browser, then press ENTER here to continue...")

        print("Verification completed. Continuing...")

        # Step 4 - Reload after human trust
        page.reload()
        time.sleep(5)

        print("Gig Creation Page should be open now")

create_gig()
