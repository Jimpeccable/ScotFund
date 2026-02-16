import asyncio
from playwright.async_api import async_playwright
import os

async def verify_v7():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        import subprocess
        server = subprocess.Popen(["python3", "-m", "http.server", "8080"])

        try:
            await asyncio.sleep(2)
            await page.goto("http://localhost:8080/index.html")
            await asyncio.sleep(2)

            # 1. Check New Only checkbox
            new_only = await page.query_selector("#report-new-only")
            if new_only:
                print("✓ 'New Only' report filter found")

            # 2. Check Select All checkbox in table
            select_all = await page.query_selector("#select-all-opps")
            if select_all:
                print("✓ 'Select All' table checkbox found")

            # 3. Open modal and check Edit Mode button
            # Since there might be no funds, I'll mock one if needed, but let's see if the layout is there.
            # I'll just check if the modal header elements are present in the DOM (hidden)
            edit_btn = await page.query_selector("#edit-mode-btn")
            if edit_btn:
                print("✓ 'Edit Mode' button found in modal")

            # 4. Screenshot the dashboard
            await page.screenshot(path="v7_dashboard.png")
            print("✓ Dashboard screenshot saved")

        finally:
            server.terminate()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_v7())
