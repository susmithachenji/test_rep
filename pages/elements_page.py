from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class AddRemoveElementsPage(BasePage):
    path = "/add-remove-elements"

    ADD_BUTTON = "button:has-text('Add Element')"
    ELEMENTS = "#elements button.added-manually"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def add_element(self) -> None:
        self.page.click(self.ADD_BUTTON)

    def add_elements(self, times: int = 1) -> None:
        for _ in range(times):
            self.add_element()

    def remove_first_element(self) -> None:
        self.page.locator(self.ELEMENTS).first.click()

    @property
    def element_count(self) -> int:
        return self.page.locator(self.ELEMENTS).count()