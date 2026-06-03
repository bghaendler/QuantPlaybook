import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"EXCEPTION: {err}"))
        
        print("Navigating to Forward & Futures Rates quiz...")
        await page.goto("http://127.0.0.1:8000/#quiz-forward-futures")
        await page.wait_for_timeout(2000)
        
        print("Submitting correct answers...")
        # Q1
        await page.fill("#qff1_input", "8.33")
        await page.click("button:has-text('Submit Answer') >> nth=0")
        
        # Q2
        await page.check("input[name='qff2_option'][value='negative']")
        await page.click("button:has-text('Submit Answer') >> nth=1")
        
        # Q3
        await page.check("input[name='qff3_option'][value='above']")
        await page.click("button:has-text('Submit Answer') >> nth=2")
        
        # Q4
        await page.check("input[name='qff4_option'][value='opt3']")
        await page.click("button:has-text('Submit Answer') >> nth=3")
        
        # Q5
        await page.check("input[name='qff5_option'][value='opt3']")
        await page.click("button:has-text('Submit Answer') >> nth=4")
        
        # Q6
        await page.check("input[name='qff6_option'][value='opt1']")
        await page.click("button:has-text('Submit Answer') >> nth=5")
        
        # Q7
        await page.check("input[name='qff7_option'][value='plus2']")
        await page.click("button:has-text('Submit Answer') >> nth=6")
        
        await page.wait_for_timeout(2000)
        
        # Take a screenshot of the entire page
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/quiz_forward_futures_verified.png", full_page=True)
        print("Saved quiz_forward_futures_verified.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
