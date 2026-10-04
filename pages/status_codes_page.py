from __future__ import annotations

from playwright.sync_api import Page, Response

from pages.base_page import BasePage


class StatusCodesPage(BasePage):
    """Pages that answer with a specific HTTP status code."""

    path = "/status-codes"

    CODES = ("200", "301", "404", "500")

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def code_link(self, code: str):
        return self.page.locator(f"#core a[href='status-codes/{code}']")

    def goto_code(self, code: str) -> Response:
        """Navigate to the status-code page and return the HTTP response."""

        return self.page.goto(f"{self.base_url}/status-codes/{code}", wait_until="domcontentloaded")