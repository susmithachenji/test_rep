from __future__ import annotations

from playwright.sync_api import Page

import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON = "#submit-login"
    FLASH_MESSAGE = "#flash"

    def __init__(self, page: Page, base_url: str = config.BASE_URL) -> None:
        super().__init__(page, base_url)

    # --- actions -----------------------------------------------------------
    def fill_username(self, username: str) -> None:
        self.page.fill(self.USERNAME_INPUT, username)

    def fill_password(self, password: str) -> None:
        self.page.fill(self.PASSWORD_INPUT, password)

    def submit(self) -> None:
        self.page.click(self.SUBMIT_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    def login_as_valid_user(self) -> None:
        self.login(config.UI_USERNAME, config.UI_PASSWORD)

    def logout(self) -> None:
        self.page.get_by_role("link", name="Logout").click()

    # --- state -------------------------------------------------------------
    @property
    def flash_message(self) -> str:
        return self.page.locator(self.FLASH_MESSAGE).inner_text().strip()

    @property
    def secure_area_greeting(self) -> str:
        return self.page.locator("#core h2").inner_text().strip()