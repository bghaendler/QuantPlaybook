import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"EXCEPTION: {err}"))
        
        print("Navigating to Forward & Futures Rates page...")
        await page.goto("http://127.0.0.1:8000/#forward-futures")
        await page.wait_for_timeout(2000)
        
        # Take a screenshot of the entire page
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/forward_futures_verified.png", full_page=True)
        print("Saved forward_futures_verified.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
