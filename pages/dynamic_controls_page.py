from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DynamicControlsPage(BasePage):
    """Checkbox / input that are swapped asynchronously (5 second delay)."""

    path = "/dynamic-controls"

    CHECKBOX_FORM = "#checkbox-example"
    INPUT_FORM = "#input-example"
    SWAP_TIMEOUT_MS = 15_000

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # --- checkbox remove/add ---------------------------------------------
    def checkbox_button_label(self) -> str:
        return self.page.locator(f"{self.CHECKBOX_FORM} button").inner_text().strip()

    def checkbox_count(self) -> int:
        return self.page.locator(f"{self.CHECKBOX_FORM} input[type=checkbox]").count()

    def click_checkbox_button(self) -> None:
        self.page.locator(f"{self.CHECKBOX_FORM} button").click()

    def wait_for_checkbox_state(self, expected_count: int) -> None:
        self.page.wait_for_function(
            "count => document.querySelectorAll('#checkbox-example input[type=checkbox]').length === count",
            arg=expected_count,
            timeout=self.SWAP_TIMEOUT_MS,
        )

    # --- input enable/disable --------------------------------------------
    def input_button_label(self) -> str:
        return self.page.locator(f"{self.INPUT_FORM} button").inner_text().strip()

    def is_input_disabled(self) -> bool:
        return self.page.locator(f"{self.INPUT_FORM} input").is_disabled()

    def click_input_button(self) -> None:
        self.page.locator(f"{self.INPUT_FORM} button").click()

    def wait_for_input_disabled(self, disabled: bool) -> None:
        self.page.wait_for_function(
            "flag => document.querySelector('#input-example input').disabled === flag",
            arg=disabled,
            timeout=self.SWAP_TIMEOUT_MS,
        )