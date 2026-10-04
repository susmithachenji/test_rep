import pytest
from playwright.sync_api import expect

import config
from pages import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.mark.smoke
def test_valid_credentials_log_into_secure_area(login_page: LoginPage) -> None:
    login_page.login_as_valid_user()

    expect(login_page.page).to_have_url(f"{config.BASE_URL}/secure")
    expect(login_page.page.get_by_role("heading", name=f"Hi, {config.UI_USERNAME}!")).to_be_visible()
    expect(login_page.page.get_by_text("Welcome to the Secure Area")).to_be_visible()
    assert login_page.page.get_by_role("link", name="Logout").is_visible()


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        (config.UI_INVALID_USERNAME, config.UI_PASSWORD, "Your username is invalid!"),
        (config.UI_USERNAME, config.UI_INVALID_PASSWORD, "Your password is invalid!"),
    ],
    ids=["invalid-username", "invalid-password"],
)
def test_invalid_credentials_show_error_message(
    login_page: LoginPage, username: str, password: str, expected_error: str
) -> None:
    login_page.login(username, password)

    expect(login_page.page).to_have_url(f"{config.BASE_URL}/login")
    expect(login_page.page.locator(LoginPage.FLASH_MESSAGE)).to_have_text(expected_error)
    assert login_page.flash_message == expected_error


@pytest.mark.smoke
def test_logout_returns_to_login_page(login_page: LoginPage) -> None:
    login_page.login_as_valid_user()
    expect(login_page.page).to_have_url(f"{config.BASE_URL}/secure")

    login_page.logout()

    expect(login_page.page).to_have_url(f"{config.BASE_URL}/login")
    expect(login_page.page.locator(LoginPage.USERNAME_INPUT)).to_be_visible()