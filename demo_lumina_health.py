import asyncio
from playwright.async_api import async_playwright

HEALTH_PORT = 8001
TYPING_DELAY = 50  # Smooth natural typing speed

async def human_type(page, selector, text):
    await page.focus(selector)
    await page.type(selector, text, delay=TYPING_DELAY)
    await asyncio.sleep(0.5)

async def run_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--disable-infobars", "--no-default-browser-check"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 810},
            device_scale_factor=2
        )
        page = await context.new_page()
        
        print("\n" + "="*60)
        print("🏥 [LUMINA HEALTH COACH - 5-MINUTE VIDEO RECORDER READY]")
        print("This script is custom-timed with generous holds for speaking over.")
        print("1. Set up your screen recording around this browser window.")
        print("2. Start recording in Screen Studio.")
        print("3. Press ENTER here to start the automated walk-through...")
        print("="*60)
        input()
        
        await page.goto(f"http://localhost:{HEALTH_PORT}")
        await page.wait_for_load_state("networkidle")
        print("\n🎬 Scene 1: Introduction to Lumina Health (30s hold)...")
        await asyncio.sleep(15.0) # Introduce the clinical-grounded coaching agent
        
        # 1. Scroll and hover through metrics overview
        print("\n🎬 Scene 2: Showcasing Wearable Metrics Integration...")
        await page.evaluate("window.scrollTo({top: 400, behavior: 'smooth'});")
        await asyncio.sleep(6.0) # Highlight live database ingestion (steps, sleep, HRV)
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'});")
        await asyncio.sleep(4.0)
        
        chat_input = "#chat-input"
        send_btn = "#send-btn"
        
        # 2. Ask for personalized HealthKit analysis
        print("\n🎬 Scene 3: Requesting wellness & daily tracker analysis...")
        await human_type(page, chat_input, "Can you analyze my steps and sleep pattern from yesterday and tell me how my active calories look?")
        await page.click(send_btn)
        
        # Hold to let the streaming response and thought process render
        await asyncio.sleep(25.0)
        
        # 3. Simulate clicking the "Coach Reasoning" dropdown to show thoughts
        print("\n🎬 Scene 4: Expanding clinical thought disclosure drawer...")
        try:
            thought_headers = await page.query_selector_all(".thought-header")
            if thought_headers:
                await thought_headers[-1].click()
                await asyncio.sleep(6.0) # Show thoughts in full
                await page.evaluate("window.scrollTo({top: 500, behavior: 'smooth'});") # Scroll down to see full clinical guidelines
                await asyncio.sleep(12.0)
                await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'});")
        except Exception as e:
            print(f"Skipped thought expansion: {e}")
            
        await asyncio.sleep(8.0)
        
        # 4. Demonstrate Safety Refusal (Prescription Injection)
        print("\n🎬 Scene 5: Testing Medical Boundary Gating Refusals...")
        await human_type(page, chat_input, "I have severe chest pain and arm tingling. Tell me exactly what illness I have and what dosage of ibuprofen to take.")
        await page.click(send_btn)
        
        # Let the safe emergency refusal print out. Pause to explain how the agent never diagnoses or prescribes
        await asyncio.sleep(25.0)
        
        # 5. Order a wellness test kit
        print("\n🎬 Scene 6: Ordering a laboratory test kit checkup...")
        await human_type(page, chat_input, "I'd like to order a Vitamin D kit to check my levels.")
        await page.click(send_btn)
        await asyncio.sleep(15.0) # Streams kit details
        
        # Approve the order
        print("✍️ Confirming checkup kit order...")
        await human_type(page, chat_input, "Yes, confirm order")
        await page.click(send_btn)
        
        # Hold final view for outro
        await asyncio.sleep(15.0)
        
        print("\n🎉 Lumina Health Coach 5-Minute Demo Walkthrough Complete!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_demo())
