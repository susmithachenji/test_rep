import re

import pytest
from playwright.sync_api import expect

from pages import AddRemoveElementsPage, CheckboxesPage, DropdownPage, InputsPage

pytestmark = pytest.mark.ui


def test_add_and_remove_elements(page) -> None:
    elements_page = AddRemoveElementsPage(page).open()

    assert elements_page.element_count == 0

    elements_page.add_elements(3)
    expect(elements_page.page.locator(AddRemoveElementsPage.ELEMENTS)).to_have_count(3)

    elements_page.remove_first_element()
    expect(elements_page.page.locator(AddRemoveElementsPage.ELEMENTS)).to_have_count(2)
    assert all(
        text.strip() == "Delete" for text in elements_page.page.locator(AddRemoveElementsPage.ELEMENTS).all_inner_texts()
    )


def test_web_inputs_display_and_clear_values(page) -> None:
    inputs_page = InputsPage(page).open()
    number, text, password, date = "42", "Playwright rocks", "Secret123", "2026-05-15"

    inputs_page.fill_inputs(number, text, password, date)
    inputs_page.display_inputs()

    result = re.sub(r"\s+", " ", inputs_page.result_text)
    assert "Output: Number 42" in result
    assert f"Output: Text {text}" in result
    assert f"Output: Password {password}" in result
    assert f"Output: Date {date}" in result

    inputs_page.clear_inputs()
    for selector in (
        InputsPage.NUMBER_INPUT,
        InputsPage.TEXT_INPUT,
        InputsPage.PASSWORD_INPUT,
        InputsPage.DATE_INPUT,
    ):
        expect(inputs_page.page.locator(selector)).to_have_value("")
    assert inputs_page.result_text == ""


def test_checkboxes_default_state_and_toggle(page) -> None:
    checkboxes = CheckboxesPage(page).open()

    assert checkboxes.is_checked("1") is False
    assert checkboxes.is_checked("2") is True

    checkboxes.set_checked("1", True)
    checkboxes.set_checked("2", False)

    assert checkboxes.is_checked("1") is True
    assert checkboxes.is_checked("2") is False


def test_dropdown_selection(page) -> None:
    dropdowns = DropdownPage(page).open()

    assert dropdowns.simple_options()[1:] == ["Option 1", "Option 2"]
    assert dropdowns.country_option_count() > 200

    dropdowns.simple_dropdown.select_option("2")
    dropdowns.country_dropdown.select_option("DE")

    expect(dropdowns.simple_dropdown).to_have_value("2")
    expect(dropdowns.country_dropdown).to_have_value("DE")