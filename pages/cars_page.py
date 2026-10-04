from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CarsShowroomPage(BasePage):
    """Cars showroom UI - it renders the data served by /api/cars."""

    path = "/cars"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open_and_wait(self) -> "CarsShowroomPage":
        self.open()
        self.page.locator("#core img").first.wait_for(state="visible")
        return self

    def car_names(self) -> list[str]:
        return [text.strip() for text in self.page.locator("#core .card-title, #core h5").all_inner_texts()]

    def car_prices(self) -> list[str]:
        return [text.strip() for text in self.page.locator("#core .card-text, #core p").all_inner_texts()]

    def image_sources(self) -> list[str]:
        return [
            src.split("/")[-1]
            for src in self.page.eval_on_selector_all(
                "#core img", "imgs => imgs.map(i => i.getAttribute('src'))"
            )
        ]