from __future__ import annotations

import config
from playwright.sync_api import Page


class BasePage:
    """Common navigation helper shared by all page objects."""

    path: str = "/"

    def __init__(self, page: Page, base_url: str = config.BASE_URL) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str | None = None) -> "BasePage":
        target = path if path is not None else self.path
        if not target.startswith("http"):
            target = f"{self.base_url}/{target.lstrip('/')}"
        self.page.goto(target, wait_until="domcontentloaded")
        return self