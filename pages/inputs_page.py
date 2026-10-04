from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class InputsPage(BasePage):
    path = "/inputs"

    NUMBER_INPUT = "#input-number"
    TEXT_INPUT = "#input-text"
    PASSWORD_INPUT = "#input-password"
    DATE_INPUT = "#input-date"
    DISPLAY_BUTTON = "#btn-display-inputs"
    CLEAR_BUTTON = "#btn-clear-inputs"
    RESULT = "#result"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def fill_inputs(
        self,
        number: str,
        text: str,
        password: str,
        date: str,
    ) -> None:
        self.page.fill(self.NUMBER_INPUT, number)
        self.page.fill(self.TEXT_INPUT, text)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.fill(self.DATE_INPUT, date)

    def display_inputs(self) -> None:
        self.page.click(self.DISPLAY_BUTTON)

    def clear_inputs(self) -> None:
        self.page.click(self.CLEAR_BUTTON)

    @property
    def result_text(self) -> str:
        return self.page.locator(self.RESULT).inner_text().strip()

    def input_value(self, selector: str) -> str:
        return self.page.input_value(selector)