import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"EXCEPTION: {err}"))
        
        print("Navigating to the home page...")
        await page.goto("http://127.0.0.1:8000/#quiz-interest-rates")
        await page.wait_for_timeout(2000)
        
        print("Verifying quiz elements...")
        # Check if the quiz container is visible
        is_visible = await page.is_visible("#view-quiz-interest-rates")
        print(f"Quiz container visible: {is_visible}")
        
        # Take a screenshot before answering
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/quiz_before_answers.png")
        print("Saved quiz_before_answers.png")
        
        # Answer Q1
        await page.fill("#qir1_input", "35")
        await page.click("button:has-text('Submit Answer') >> nth=0")
        
        # Answer Q2
        await page.fill("#qir2_input", "8.11")
        await page.click("button:has-text('Submit Answer') >> nth=1")
        
        # Answer Q3 (Decrease)
        await page.check("input[name='qir3_option'][value='decrease']")
        await page.click("button:has-text('Submit Answer') >> nth=2")
        
        # Answer Q4 (No)
        await page.check("input[name='qir4_option'][value='no']")
        await page.click("button:has-text('Submit Answer') >> nth=3")
        
        # Answer Q5 (True)
        await page.check("input[name='qir5_option'][value='true']")
        await page.click("button:has-text('Submit Answer') >> nth=4")
        
        # Answer Q6 (False)
        await page.check("input[name='qir6_option'][value='false']")
        await page.click("button:has-text('Submit Answer') >> nth=5")
        
        # Answer Q7 (Statement 1, 3, 4)
        await page.check("input[name='qir7_option'][value='qir7_1']")
        await page.check("input[name='qir7_option'][value='qir7_3']")
        await page.check("input[name='qir7_option'][value='qir7_4']")
        await page.click("button:has-text('Submit Answer') >> nth=6")
        
        # Answer Q8 (Statement 2)
        await page.check("input[name='qir8_option'][value='qir8_2']")
        await page.click("button:has-text('Submit Answer') >> nth=7")
        
        await page.wait_for_timeout(2000)
        
        # Take a screenshot after answering to verify all are green and correct!
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/quiz_after_answers.png", full_page=True)
        print("Saved quiz_after_answers.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
