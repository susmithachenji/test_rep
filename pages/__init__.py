"""Page objects for the practice site.

Each class wraps one demo page and exposes stable locators so the tests stay
free of CSS/XPath details.
"""

from pages.base_page import BasePage
from pages.checkboxes_page import CheckboxesPage
from pages.cars_page import CarsShowroomPage
from pages.dropdown_page import DropdownPage
from pages.dynamic_controls_page import DynamicControlsPage
from pages.dynamic_table_page import DynamicTablePage
from pages.elements_page import AddRemoveElementsPage
from pages.inputs_page import InputsPage
from pages.js_dialogs_page import JsDialogsPage
from pages.login_page import LoginPage
from pages.notification_page import NotificationMessagePage
from pages.sortable_table_page import SortableTablePage
from pages.status_codes_page import StatusCodesPage

__all__ = [
    "AddRemoveElementsPage",
    "BasePage",
    "CarsShowroomPage",
    "CheckboxesPage",
    "DropdownPage",
    "DynamicControlsPage",
    "DynamicTablePage",
    "InputsPage",
    "JsDialogsPage",
    "LoginPage",
    "NotificationMessagePage",
    "SortableTablePage",
    "StatusCodesPage",
]