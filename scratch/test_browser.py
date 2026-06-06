import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_errors = []
        console_messages = []

        # Listen for console messages
        def on_console(msg):
            text = f"[{msg.type}] {msg.text}"
            console_messages.append(text)
            if msg.type == "error":
                console_errors.append(msg.text)
                print("BROWSER ERROR:", msg.text)
            else:
                print("BROWSER LOG:", msg.text)

        page.on("console", on_console)

        # 1. Load root page
        print("--- Loading http://127.0.0.1:8000/ ---")
        await page.goto("http://127.0.0.1:8000/", wait_until="load")
        await asyncio.sleep(2)  # Wait for initial typesetting to settle

        # 2. Go to #cqf-dashboard
        print("--- Navigating to #cqf-dashboard ---")
        await page.evaluate("showSection('cqf-dashboard')")
        await asyncio.sleep(2)

        # 3. Go to #cqf-mp-linalg
        print("--- Navigating to #cqf-mp-linalg ---")
        await page.evaluate("showSection('cqf-mp-linalg')")
        await asyncio.sleep(2)

        # 4. Click the Worked Solutions tab directly by ID
        print("--- Clicking Worked Solutions tab ---")
        try:
            await page.click("#tabLinAlgExercises")
            print("Successfully clicked Worked Solutions Sheet tab!")
            await asyncio.sleep(2)
        except Exception as e:
            print("Failed to click tab:", e)

        # 5. Go to #cqf-mp-calculus
        print("--- Navigating to #cqf-mp-calculus ---")
        await page.evaluate("showSection('cqf-mp-calculus')")
        await asyncio.sleep(2)

        # 6. Go to #interest-rates
        print("--- Navigating to #interest-rates ---")
        await page.evaluate("showSection('interest-rates')")
        await asyncio.sleep(2)

        await browser.close()

        print("\n=== SUMMARY OF CONSOLE ERRORS ===")
        if not console_errors:
            print("No console errors detected! Pure success.")
        else:
            for err in console_errors:
                print("-", err)

asyncio.run(run())
