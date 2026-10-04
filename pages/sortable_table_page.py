from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class SortableTablePage(BasePage):
    """Clicking a table header sorts the column (DataTables behaviour)."""

    path = "/tables"

    TABLE = "#table1"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def headers(self) -> list[str]:
        return [text.strip() for text in self.page.locator(f"{self.TABLE} thead th").all_inner_texts()]

    def row_count(self) -> int:
        return self.page.locator(f"{self.TABLE} tbody tr").count()

    def sort_by(self, column: str) -> None:
        index = self.headers().index(column)
        self.page.locator(f"{self.TABLE} thead th").nth(index).click()
        self.page.wait_for_timeout(600)

    def column_values(self, column: str) -> list[str]:
        index = self.headers().index(column)
        return [
            row.strip()
            for row in self.page.locator(f"{self.TABLE} tbody tr").evaluate_all(
                "(rows, index) => rows.map(row => row.cells[index].textContent.trim())",
                index,
            )
        ]