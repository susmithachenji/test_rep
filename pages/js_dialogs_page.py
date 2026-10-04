from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class JsDialogsPage(BasePage):
    path = "/js-dialogs"

    ALERT_BUTTON = "#js-alert"
    CONFIRM_BUTTON = "#js-confirm"
    PROMPT_BUTTON = "#js-prompt"
    RESPONSE = "#dialog-response"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def click_with_dialog(
        self,
        button: str,
        accept: bool = True,
        prompt_text: str | None = None,
    ) -> str:
        """Click a dialog button, handle the JS dialog and return the page response."""

        def handler(dialog) -> None:
            if not accept:
                dialog.dismiss()
            elif prompt_text is None:
                dialog.accept()
            else:
                dialog.accept(prompt_text)

        self.page.once("dialog", handler)
        self.page.click(button)
        return self.page.locator(self.RESPONSE).inner_text().strip()