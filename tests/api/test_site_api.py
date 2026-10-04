import pytest

from clients.site_api_client import SiteApiClient

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_notes_api_health_check_is_up(api: SiteApiClient) -> None:
    response = api.notes_health_check()

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["status"] == 200
    assert body["message"] == "Notes API is Running"


@pytest.mark.smoke
def test_cars_api_returns_six_cars(api: SiteApiClient) -> None:
    response = api.get_cars()

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"

    cars = body["cars"]
    assert len(cars) == 6
    assert [car["id"] for car in cars] == [1, 2, 3, 4, 5, 6]
    assert cars[0]["name"] == "VW Golf"
    assert cars[0]["price"].startswith("€")
    assert all(car["image"].startswith("/img/cars/") for car in cars)


def test_status_code_pages_over_http(api: SiteApiClient) -> None:
    assert api.get_page_status("status-codes/200") == 200
    assert api.get_page_status("status-codes/301") == 301
    assert api.get_page_status("status-codes/404") == 404
    assert api.get_page_status("status-codes/500") == 500