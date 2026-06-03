import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"EXCEPTION: {err}"))
        
        print("Navigating...")
        await page.goto("http://127.0.0.1:8000/#interest-rates")
        await page.wait_for_timeout(2000)
        
        # Verify sizes of elements
        eval_result = await page.evaluate("""() => {
            const results = {};
            const card1 = document.querySelector("div.card:has(#interestRatesChart)");
            const card2 = document.querySelector("div.card:has(#moneyMarketChart)");
            const canvas1 = document.getElementById("interestRatesChart");
            const canvas2 = document.getElementById("discountCurveChart");
            const canvas3 = document.getElementById("moneyMarketChart");
            
            results.card1_width = card1 ? card1.clientWidth : 0;
            results.card2_width = card2 ? card2.clientWidth : 0;
            results.canvas1_width = canvas1 ? canvas1.clientWidth : 0;
            results.canvas2_width = canvas2 ? canvas2.clientWidth : 0;
            results.canvas3_width = canvas3 ? canvas3.clientWidth : 0;
            
            return results;
        }""")
        
        print("\n--- FIXED ELEMENT WIDTHS ---")
        for k, v in eval_result.items():
            print(f"{k}: {v}px")
        print("----------------------------\n")
        
        # Capture updated card screenshots for visual validation
        print("Taking screenshots...")
        try:
            card1 = page.locator("div.card:has(#interestRatesChart)")
            await card1.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/fixed_term_structure_charts.png")
            print("Saved fixed term structure charts screenshot")
        except Exception as e:
            print(f"Error capturing card1: {e}")
            
        try:
            card2 = page.locator("div.card:has(#moneyMarketChart)")
            await card2.screenshot(path="/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/fixed_money_market_charts.png")
            print("Saved fixed money market charts screenshot")
        except Exception as e:
            print(f"Error capturing card2: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
