import pytest

from clients.site_api_client import SiteApiClient
from pages import CarsShowroomPage

pytestmark = [pytest.mark.ui, pytest.mark.api]


def test_cars_showroom_renders_api_data(page, api: SiteApiClient) -> None:
    """UI test that cross-checks the rendered cars against the /api/cars payload."""

    expected_cars = api.get_cars().json()["cars"]

    showroom = CarsShowroomPage(page).open_and_wait()
    rendered_images = showroom.image_sources()

    assert len(rendered_images) == len(expected_cars)
    assert rendered_images == [car["image"].split("/")[-1] for car in expected_cars]

    body_text = showroom.page.locator("#core").inner_text()
    for car in expected_cars:
        assert car["name"] in body_text