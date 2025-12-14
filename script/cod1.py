import asyncio
import random
from dataclasses import dataclass
from playwright.async_api import async_playwright, Page


# ================= CONFIG =================

@dataclass
class BookingConfig:
    target_url: str
    headless: bool = True
    delay_range: tuple = (1, 3)


# ================= AGENT =================

class EdreamsTestAgent:

    def __init__(self, config: BookingConfig):
        self.config = config

    async def random_delay(self):
        await asyncio.sleep(random.uniform(*self.config.delay_range))

    async def accept_cookies(self, page: Page):
        try:
            await page.wait_for_selector(
                'button:has-text("Accepter"), button:has-text("Accept")',
                timeout=5000
            )
            await page.click('button:has-text("Accepter"), button:has-text("Accept")')
            print("[COOKIES] Accepted ✅")
        except:
            print("[COOKIES] No cookie banner")

    async def verify_page_loaded(self, page: Page):
        title = await page.title()
        print("[DEBUG] Page title:", title)

        if "eDreams" in title or "Ryanair" in title:
            print("[PAGE] Correct page loaded ✅")
        else:
            print("[PAGE] Unexpected page ❌")

        print("[DEBUG] Current URL:", page.url)

    async def detect_inputs(self, page: Page):
        inputs = await page.query_selector_all("input")
        print(f"[PAGE] Found {len(inputs)} input fields")

        if len(inputs) > 0:
            print("[PAGE] Page is interactive ✅")
        else:
            print("[PAGE] No inputs found (possible block) ❌")

    async def human_behavior(self, page: Page):
        await page.mouse.move(
            random.randint(100, 600),
            random.randint(100, 600)
        )
        await page.evaluate("window.scrollBy(0, 300)")
        await self.random_delay()

    async def run(self):
        print("[AGENT] Starting eDreams test agent")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.config.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )

            page = await context.new_page()

            print("[AGENT] Navigating to target URL")
            await page.goto(self.config.target_url, wait_until="networkidle")

            await self.accept_cookies(page)
            await self.random_delay()

            await self.verify_page_loaded(page)
            await self.detect_inputs(page)
            await self.human_behavior(page)

            print("[AGENT] Test finished successfully ✅")

            await context.close()
            await browser.close()


# ================= MAIN =================

async def main():
    config = BookingConfig(
        target_url="https://www.edreams.fr/offres/vol/compagnie-aerienne/FR/ryanair/",
        headless=True
    )

    agent = EdreamsTestAgent(config)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
