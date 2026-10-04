from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DropdownPage(BasePage):
    path = "/dropdown"

    SIMPLE_DROPDOWN = "#dropdown"
    COUNTRY_DROPDOWN = "#country"
    ELEMENTS_PER_PAGE = "#elementsPerPageSelect"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def simple_dropdown(self):
        return self.page.locator(self.SIMPLE_DROPDOWN)

    @property
    def country_dropdown(self):
        return self.page.locator(self.COUNTRY_DROPDOWN)

    @property
    def elements_per_page_dropdown(self):
        return self.page.locator(self.ELEMENTS_PER_PAGE)

    def simple_options(self) -> list[str]:
        return [
            value.strip()
            for value in self.page.eval_on_selector_all(
                f"{self.SIMPLE_DROPDOWN} option", "els => els.map(e => e.textContent)"
            )
        ]

    def country_option_count(self) -> int:
        return self.page.locator(f"{self.COUNTRY_DROPDOWN} option").count()