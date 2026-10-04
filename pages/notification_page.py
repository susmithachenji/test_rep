from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class NotificationMessagePage(BasePage):
    path = "/notification-message"

    FLASH = "#flash-message"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def flash_message(self) -> str:
        return self.page.locator(self.FLASH).inner_text().strip()

    def load_another_message(self) -> None:
        self.page.get_by_role("link", name="Click here").click()