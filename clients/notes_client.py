"""HTTP client for the Notes REST API.

Base URL: https://practice.expandtesting.com/notes/api
Swagger:  https://practice.expandtesting.com/notes/api/swagger.json

Notes
-----
* every protected endpoint expects the token in the ``x-auth-token`` header
* ``register`` does **not** return a token -> log in afterwards
* validation failures answer with HTTP 400 and a ``message`` field
"""

from __future__ import annotations

from typing import Any

import requests

import config


class NotesClient:
    def __init__(
        self,
        base_url: str = config.NOTES_API_URL,
        timeout: float = config.API_TIMEOUT_S,
        token: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token = token
        self.credentials: dict[str, str] = {}
        self.session = requests.Session()

    # --- helpers -----------------------------------------------------------
    @property
    def headers(self) -> dict[str, str]:
        return {"x-auth-token": self.token} if self.token else {}

    def set_token(self, token: str) -> None:
        self.token = token

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    # --- users -------------------------------------------------------------
    def register(self, name: str, email: str, password: str) -> requests.Response:
        self.credentials = {"name": name, "email": email, "password": password}
        return self.session.post(
            self._url("users/register"),
            data={"name": name, "email": email, "password": password},
            timeout=self.timeout,
        )

    def login(self, email: str, password: str) -> requests.Response:
        return self.session.post(
            self._url("users/login"),
            data={"email": email, "password": password},
            timeout=self.timeout,
        )

    def login_and_store_token(self, email: str, password: str) -> str:
        response = self.login(email, password)
        response.raise_for_status()
        token = response.json()["data"]["token"]
        self.set_token(token)
        return token

    def get_profile(self) -> requests.Response:
        return self.session.get(self._url("users/profile"), headers=self.headers, timeout=self.timeout)

    def logout(self) -> requests.Response:
        return self.session.delete(self._url("users/logout"), headers=self.headers, timeout=self.timeout)

    def delete_account(self) -> requests.Response:
        return self.session.delete(self._url("users/delete-account"), headers=self.headers, timeout=self.timeout)

    # --- notes -------------------------------------------------------------
    def create_note(self, title: str, description: str, category: str) -> requests.Response:
        return self.session.post(
            self._url("notes"),
            headers=self.headers,
            data={"title": title, "description": description, "category": category},
            timeout=self.timeout,
        )

    def list_notes(self) -> requests.Response:
        return self.session.get(self._url("notes"), headers=self.headers, timeout=self.timeout)

    def get_note(self, note_id: str) -> requests.Response:
        return self.session.get(self._url(f"notes/{note_id}"), headers=self.headers, timeout=self.timeout)

    def update_note(
        self,
        note_id: str,
        title: str,
        description: str,
        category: str,
        completed: bool,
    ) -> requests.Response:
        return self.session.put(
            self._url(f"notes/{note_id}"),
            headers=self.headers,
            json={
                "title": title,
                "description": description,
                "category": category,
                "completed": completed,
            },
            timeout=self.timeout,
        )

    def set_note_completed(self, note_id: str, completed: bool) -> requests.Response:
        return self.session.patch(
            self._url(f"notes/{note_id}"),
            headers=self.headers,
            json={"completed": completed},
            timeout=self.timeout,
        )

    def delete_note(self, note_id: str) -> requests.Response:
        return self.session.delete(self._url(f"notes/{note_id}"), headers=self.headers, timeout=self.timeout)

    # --- convenience -------------------------------------------------------
    def create_sample_note(self, title: str = "Playwright sample note", **overrides: Any) -> dict:
        payload = {
            "title": title,
            "description": "Created by an automated test run",
            "category": "Home",
        }
        payload.update(overrides)
        response = self.create_note(**payload)
        response.raise_for_status()
        return response.json()["data"]