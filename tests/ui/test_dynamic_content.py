import re

import pytest

from pages import DynamicControlsPage, DynamicTablePage, SortableTablePage

pytestmark = pytest.mark.ui


def test_dynamic_table_shows_randomised_task_manager_data(page) -> None:
    table = DynamicTablePage(page).open()

    assert table.description == "Task Manager"
    assert set(table.headers()) == {"Name", "Network", "CPU", "Disk", "Memory"}
    assert table.row_count() == 4
    assert set(table.row_names()) == {"System", "Internet Explorer", "Firefox", "Chrome"}

    # the yellow label always mirrors the CPU value of the Chrome row
    label_value = re.search(r"([\d.]+%)", table.chrome_cpu_label()).group(1)
    assert table.cell_value("Chrome", "CPU") == label_value


def test_sortable_table_sorts_by_last_name(page) -> None:
    table = SortableTablePage(page).open()

    assert table.headers()[0] == "Last Name"
    assert table.row_count() == 4

    table.sort_by("Last Name")
    assert table.column_values("Last Name") == sorted(table.column_values("Last Name"))

    table.sort_by("Last Name")
    assert table.column_values("Last Name") == sorted(table.column_values("Last Name"), reverse=True)


def test_dynamic_controls_swap_checkbox_and_input(page) -> None:
    controls = DynamicControlsPage(page).open()

    assert controls.checkbox_button_label() == "Remove"
    assert controls.checkbox_count() == 1
    assert controls.input_button_label() == "Enable"
    assert controls.is_input_disabled() is True

    controls.click_checkbox_button()
    controls.wait_for_checkbox_state(0)
    assert controls.checkbox_button_label() == "Add"

    controls.click_checkbox_button()
    controls.wait_for_checkbox_state(1)
    assert controls.checkbox_button_label() == "Remove"

    controls.click_input_button()
    controls.wait_for_input_disabled(False)
    assert controls.input_button_label() == "Disable"
    assert controls.is_input_disabled() is False