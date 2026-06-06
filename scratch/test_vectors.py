import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_errors = []
        console_messages = []

        def on_console(msg):
            text = f"[{msg.type}] {msg.text}"
            console_messages.append(text)
            print("BROWSER:", text)

        page.on("console", on_console)

        print("--- Loading http://127.0.0.1:8000/ ---")
        await page.goto("http://127.0.0.1:8000/", wait_until="load")
        await asyncio.sleep(2)

        print("--- Navigating to #cqf-mp-linalg-vectors ---")
        await page.evaluate("showSection('cqf-mp-linalg-vectors')")
        await asyncio.sleep(5)  # Wait longer to see if it typesets or struggles

        # Inspect if formulas are rendered
        has_mjx_container = await page.evaluate("document.querySelector('mjx-container') !== null")
        print("MathJax rendered container exists:", has_mjx_container)

        # Print outerHTML of the subtitle to see if it has been transformed
        subtitle_html = await page.evaluate("document.querySelector('#view-cqf-mp-linalg-vectors .subtitle').outerHTML")
        print("Subtitle HTML:", subtitle_html)

        await browser.close()

asyncio.run(run())
