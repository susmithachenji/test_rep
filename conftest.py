"""Shared pytest fixtures: Playwright browser/page and API clients."""

from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

import config
from clients.notes_client import NotesClient
from clients.site_api_client import SiteApiClient

ARTIFACTS_DIR = Path(__file__).resolve().parent / "reports" / "artifacts"


# ---------------------------------------------------------------------------
# failure artefacts
# ---------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def page(request: pytest.FixtureRequest) -> Page:
    context: BrowserContext = request.getfixturevalue("context")
    page = context.new_page()
    page.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    yield page
    if getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed:
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=ARTIFACTS_DIR / f"{request.node.name}.png", full_page=True)
    context.close()


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    """Fresh context per test (isolated cookies / storage)."""

    ctx = browser.new_context(
        viewport={"width": 1366, "height": 900},
        ignore_https_errors=True,
    )
    ctx.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    # the page is full of ads - blocking them makes the suite fast and stable
    for pattern in config.BLOCKED_URL_PATTERNS:
        ctx.route(pattern, lambda route: route.abort())
    return ctx


# ---------------------------------------------------------------------------
# API fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def site_api() -> SiteApiClient:
    return SiteApiClient()


@pytest.fixture
def api() -> SiteApiClient:
    """Per-test public API client."""

    return SiteApiClient()


@pytest.fixture
def registered_user() -> dict[str, str]:
    return {
        "name": config.TEST_USER_NAME,
        "email": config.unique_email(),
        "password": config.TEST_USER_PASSWORD,
    }


@pytest.fixture
def registered_notes_api(registered_user: dict[str, str]) -> NotesClient:
    """Client for a brand new account (no token yet); account removed afterwards."""

    client = NotesClient()
    response = client.register(**registered_user)
    assert response.status_code == 201, response.text
    yield client
    client.login_and_store_token(registered_user["email"], registered_user["password"])
    client.delete_account()


@pytest.fixture
def notes_api(registered_notes_api: NotesClient) -> NotesClient:
    """Notes API client already registered, logged in and holding a token."""

    registered_notes_api.login_and_store_token(
        registered_notes_api.credentials["email"], registered_notes_api.credentials["password"]
    )
    return registered_notes_api


@pytest.fixture
def anonymous_notes_api() -> NotesClient:
    return NotesClient()