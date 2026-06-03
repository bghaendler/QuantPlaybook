import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"EXCEPTION: {err}"))
        
        # 1. Verify Coupon Bonds & Swaps Theory Page
        print("Navigating to #coupon-swaps...")
        await page.goto("http://127.0.0.1:8000/#coupon-swaps")
        await page.wait_for_timeout(2000)
        
        is_theory_visible = await page.is_visible("#view-coupon-swaps")
        print(f"Coupon Swaps Theory visible: {is_theory_visible}")
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/coupon_swaps_theory.png", full_page=True)
        print("Saved coupon_swaps_theory.png")

        # 2. Verify Coupon Bonds & Swaps Quiz
        print("Navigating to #quiz-coupon-swaps...")
        await page.goto("http://127.0.0.1:8000/#quiz-coupon-swaps")
        await page.wait_for_timeout(2000)
        
        is_quiz_visible = await page.is_visible("#view-quiz-coupon-swaps")
        print(f"Coupon Swaps Quiz visible: {is_quiz_visible}")
        
        # Fill in answers
        print("Answering Coupon Swaps Quiz...")
        await page.fill("#qcs1_input", "105.32")
        await page.click("#view-quiz-coupon-swaps button[onclick='checkQcs1()']")
        
        await page.check("input[name='qcs2_option'][value='B']")
        await page.click("#view-quiz-coupon-swaps button[onclick='checkQcs2()']")
        
        await page.fill("#qcs3_input", "5.51")
        await page.click("#view-quiz-coupon-swaps button[onclick='checkQcs3()']")
        
        await page.check("input[name='qcs4_option'][value='B']")
        await page.click("#view-quiz-coupon-swaps button[onclick='checkQcs4()']")
        
        await page.check("input[name='qcs5_option'][value='true']")
        await page.click("#view-quiz-coupon-swaps button[onclick='checkQcs5()']")
        
        await page.wait_for_timeout(1000)
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/coupon_swaps_quiz_graded.png", full_page=True)
        print("Saved coupon_swaps_quiz_graded.png")

        # 3. Verify Duration & Convexity Theory Page
        print("Navigating to #duration-convexity...")
        await page.goto("http://127.0.0.1:8000/#duration-convexity")
        await page.wait_for_timeout(2000)
        
        is_dc_visible = await page.is_visible("#view-duration-convexity")
        print(f"Duration Convexity Theory visible: {is_dc_visible}")
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/duration_convexity_theory.png", full_page=True)
        print("Saved duration_convexity_theory.png")

        # 4. Verify Duration & Convexity Quiz
        print("Navigating to #quiz-duration-convexity...")
        await page.goto("http://127.0.0.1:8000/#quiz-duration-convexity")
        await page.wait_for_timeout(2000)
        
        is_dc_quiz_visible = await page.is_visible("#view-quiz-duration-convexity")
        print(f"Duration Convexity Quiz visible: {is_dc_quiz_visible}")
        
        # Fill in answers
        print("Answering Duration Convexity Quiz...")
        await page.check("input[name='qdc1_option'][value='C']")
        await page.click("#view-quiz-duration-convexity button[onclick='checkQdc1()']")
        
        await page.fill("#qdc2_input", "-8.06")
        await page.click("#view-quiz-duration-convexity button[onclick='checkQdc2()']")
        
        await page.fill("#qdc3_input", "-2.14")
        await page.click("#view-quiz-duration-convexity button[onclick='checkQdc3()']")
        
        await page.fill("#qdc4_input", "-11.81")
        await page.click("#view-quiz-duration-convexity button[onclick='checkQdc4()']")
        
        await page.check("input[name='qdc5_option'][value='A']")
        await page.click("#view-quiz-duration-convexity button[onclick='checkQdc5()']")
        
        await page.wait_for_timeout(1000)
        await page.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/duration_convexity_quiz_graded.png", full_page=True)
        print("Saved duration_convexity_quiz_graded.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
