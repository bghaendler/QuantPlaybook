import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://127.0.0.1:8000/", wait_until="load")
        await asyncio.sleep(2)

        # Print initial states
        print("Initial active section:", await page.evaluate("_activeSection"))
        print("Initial linalg display:", await page.evaluate("document.getElementById('view-cqf-mp-linalg').style.display"))
        print("Initial button display:", await page.evaluate("window.getComputedStyle(document.getElementById('tabLinAlgExercises')).display"))

        # Navigate
        await page.evaluate("showSection('cqf-mp-linalg')")
        await asyncio.sleep(1)

        print("After showSection active section:", await page.evaluate("_activeSection"))
        print("After showSection linalg display:", await page.evaluate("document.getElementById('view-cqf-mp-linalg').style.display"))
        print("After showSection button display:", await page.evaluate("window.getComputedStyle(document.getElementById('tabLinAlgExercises')).display"))
        
        # Check parent node chain visibility
        parent_info = await page.evaluate("""
            let el = document.getElementById('tabLinAlgExercises');
            let info = [];
            while(el) {
                info.push({
                    tag: el.tagName,
                    id: el.id,
                    display: window.getComputedStyle(el).display,
                    visibility: window.getComputedStyle(el).visibility,
                    opacity: window.getComputedStyle(el).opacity,
                    rect: el.getBoundingClientRect()
                });
                el = el.parentElement;
            }
            info;
        """)
        for item in parent_info:
            print(f"Tag: {item['tag']}, ID: {item['id']}, Display: {item['display']}, Vis: {item['visibility']}, Rect: {item['rect']}")

        await browser.close()

asyncio.run(run())
