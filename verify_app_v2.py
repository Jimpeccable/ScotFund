import asyncio
from playwright.async_api import async_playwright
import os

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # Load the local index.html
        path = os.path.abspath("index.html")
        await page.goto(f"file://{path}")

        print("Verifying Login Flow...")
        # Check if login modal is visible
        await page.wait_for_selector("#login-modal", state="visible")

        # Fill in login details
        await page.fill("#login-name", "Jules Engineer")
        await page.fill("#login-org", "Scottish Tech Charity")
        await page.fill("#login-pwd", "securepassword123")
        await page.select_option("#login-role", "Super User")
        await page.click("button:has-text('Start Using ScotFund Pro')")

        # Verify Dashboard is visible
        await page.wait_for_selector("#dashboard", state="visible")
        print("Login Successful. Dashboard visible.")
        await page.screenshot(path="/home/jules/verification/01_dashboard_logged_in.png")

        # Navigate to Profile and check new fields
        print("Verifying Profile Fields...")
        await page.click("button[data-id='profile']")
        await page.wait_for_selector("#profile", state="visible")
        await page.wait_for_selector("#profile-charity-no")
        await page.wait_for_selector("#profile-staff-count")
        await page.wait_for_selector("#profile-turnover")
        print("Profile fields verified.")
        await page.screenshot(path="/home/jules/verification/02_profile_expanded.png")

        # Navigate to Super User Dashboard
        print("Verifying Super User Dashboard...")
        await page.click("#nav-superuser")
        await page.wait_for_selector("#superuser", state="visible")

        # Check Future Requirments Tab
        print("Checking Future Requirments...")
        await page.click("#super-tab-future")
        await page.wait_for_selector("#super-panel-future", state="visible")
        content = await page.inner_text("#super-panel-future")
        if "Supabase" in content and "MongoDB" in content:
            print("Future Requirments content verified.")
        else:
            print("Warning: Future Requirments content missing keywords.")
        await page.screenshot(path="/home/jules/verification/03_future_requirements.png")

        # Check System Health Tab (Audit Log & User Management)
        print("Checking System Health & Audit Log...")
        await page.click("#super-tab-admin")
        await page.wait_for_selector("#super-panel-admin", state="visible")
        await page.wait_for_selector("#super-audit-log")
        await page.wait_for_selector("h4:has-text('User Management Simulation')")
        print("System Health verified.")
        await page.screenshot(path="/home/jules/verification/04_system_health.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_verification())
