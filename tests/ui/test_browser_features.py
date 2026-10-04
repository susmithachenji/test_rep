import pytest

from pages import JsDialogsPage, NotificationMessagePage, StatusCodesPage

pytestmark = pytest.mark.ui


def test_javascript_dialogs_are_handled(page) -> None:
    dialogs = JsDialogsPage(page).open()

    assert dialogs.click_with_dialog(JsDialogsPage.ALERT_BUTTON, accept=False) == "OK"
    assert dialogs.click_with_dialog(JsDialogsPage.CONFIRM_BUTTON, accept=True) == "Ok"
    assert dialogs.click_with_dialog(JsDialogsPage.CONFIRM_BUTTON, accept=False) == "Cancel"
    assert dialogs.click_with_dialog(JsDialogsPage.PROMPT_BUTTON, prompt_text="Playwright") == "Playwright"


def test_status_code_pages_return_expected_codes(page) -> None:
    status_codes = StatusCodesPage(page).open()

    for code in StatusCodesPage.CODES:
        response = status_codes.goto_code(code)
        assert response is not None, f"no response for status code {code}"
        assert response.status == int(code), f"expected HTTP {code}, got {response.status}"

    status_codes.open()
    assert status_codes.code_link("404").is_visible()


def test_notification_message_flash_is_displayed(page) -> None:
    notifications = NotificationMessagePage(page).open()

    assert notifications.flash_message
    assert "successful" in notifications.flash_message.lower()

    notifications.load_another_message()
    assert notifications.flash_message