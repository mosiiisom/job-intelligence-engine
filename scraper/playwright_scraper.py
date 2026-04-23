import random
import time
from playwright.sync_api import sync_playwright, Page


class PlaywrightEngine:
    def __init__(self, headless: bool = False, proxies=None, user_agents=None):
        self.headless = headless
        self.proxies = proxies or []
        self.user_agents = user_agents or []

        self.playwright = None
        self.browser = None

    def start(self):
        self.playwright = sync_playwright().start()

        proxy = self._get_proxy()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            proxy=proxy,
        )

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _get_proxy(self):
        if not self.proxies:
            return None

        return {"server": random.choice(self.proxies)}

    def _get_user_agent(self):
        if not self.user_agents:
            return None
        return random.choice(self.user_agents)

    def fetch_page(self, url: str, retries=3, delay=2):
        page = self.get_page(url, retries, delay)
        if page:
            return page.content()

        return None

    def get_page(self, url: str, retries=3, delay=2) -> Page | None:
        for attempt in range(retries):
            try:
                context = self.browser.new_context(
                    user_agent=self._get_user_agent(),
                )

                page = context.new_page()
                page.goto(url)
                page.wait_for_load_state("networkidle")

                return page
            except Exception as e:
                print(f"[ Retry {attempt + 1}] Error {e}")
                time.sleep(delay)

        return None
