from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DynamicTablePage(BasePage):
    """Task-manager style table: column order and cell values are random."""

    path = "/dynamic-table"

    DESCRIPTION = "#table-description"
    CHROME_CPU_LABEL = "#chrome-cpu"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def description(self) -> str:
        return self.page.locator(self.DESCRIPTION).inner_text().strip()

    def headers(self) -> list[str]:
        return [text.strip() for text in self.page.locator("table thead th").all_inner_texts()]

    def row_names(self) -> list[str]:
        return [text.strip() for text in self.page.locator("table tbody tr td:first-child").all_inner_texts()]

    def row_count(self) -> int:
        return self.page.locator("table tbody tr").count()

    def cell_value(self, process_name: str, column: str) -> str:
        """Read a single cell, e.g. cell_value('Chrome', 'CPU')."""

        header_index = self.headers().index(column)
        row = self.page.locator("table tbody tr", has_text=process_name).first
        return row.locator("td").nth(header_index).inner_text().strip()

    def chrome_cpu_label(self) -> str:
        return self.page.locator(self.CHROME_CPU_LABEL).inner_text().strip()