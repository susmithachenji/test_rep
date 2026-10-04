"""Small typed-ish wrappers around the public and Notes REST APIs."""

from clients.notes_client import NotesClient
from clients.site_api_client import SiteApiClient

__all__ = ["NotesClient", "SiteApiClient"]