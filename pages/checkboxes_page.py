from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckboxesPage(BasePage):
    path = "/checkboxes"

    CHECKBOX_1 = "#checkbox1"
    CHECKBOX_2 = "#checkbox2"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def locator(self, which: str = "1"):
        selector = self.CHECKBOX_1 if which == "1" else self.CHECKBOX_2
        return self.page.locator(selector)

    def is_checked(self, which: str = "1") -> bool:
        return self.locator(which).is_checked()

    def set_checked(self, which: str = "1", checked: bool = True) -> None:
        checkbox = self.locator(which)
        if checkbox.is_checked() != checked:
            checkbox.click()