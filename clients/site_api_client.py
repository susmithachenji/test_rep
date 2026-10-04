"""HTTP client for the public (unauthenticated) endpoints of the site."""

from __future__ import annotations

import requests

import config


class SiteApiClient:
    """Endpoints that do not require authentication."""

    def __init__(self, base_url: str = config.BASE_URL, timeout: float = config.API_TIMEOUT_S) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    # --- Notes API ---------------------------------------------------------
    def notes_health_check(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/notes/api/health-check", timeout=self.timeout)

    # --- Cars API ----------------------------------------------------------
    def get_cars(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/cars", timeout=self.timeout)

    # --- misc --------------------------------------------------------------
    def get_my_ip(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/my-ip/", timeout=self.timeout)

    def get_page_status(self, path: str) -> int:
        """Return the HTTP status code of a web page (no redirect following)."""

        return self.session.get(
            f"{self.base_url}/{path.lstrip('/')}",
            timeout=self.timeout,
            allow_redirects=False,
        ).status_code