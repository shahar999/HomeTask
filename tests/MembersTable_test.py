import pytest
import random
from playwright.sync_api import Page, expect, sync_playwright
from pages.MembersTablePage import MembersTablePage


class TestMembersTable:
    @pytest.fixture()
    def open_website(self, page: Page):
        names_table = MembersTablePage(page)
        names_table.navigate_to_table()

    @pytest.mark.parametrize('page_num', range(1, 11))
    def test_page_data_with_page_input_field(self, open_website, page_num, page: Page) -> None:
        members_table = MembersTablePage(page)
        if page_num != 1:
            members_table.insert_page(page_num)
        assert members_table.get_current_page_number() == page_num, 'page number didn\'t changed'
        table_from_api = members_table.get_table_from_api(page_num)
        table_from_ui = members_table.get_table_data()
        assert table_from_ui == table_from_api, 'the data in the table in page ' + str(
            page_num) + 'is not equal to the API data'

    @pytest.mark.parametrize('page_num', range(1,11))
    def test_page_data_with_next_button_navigation(self, open_website, page_num, page: Page) -> None:
        members_table = MembersTablePage(page)
        if page_num != 1:
            members_table.insert_page(page_num - 1)
            members_table.click_next_button()
        assert members_table.get_current_page_number() == page_num, 'page number didn\'t changed'
        table_from_api = members_table.get_table_from_api(page_num)
        table_from_ui = members_table.get_table_data()
        assert table_from_ui == table_from_api, 'the data in the table in page ' + str(page_num) + 'is not equal to the API data'

    @pytest.mark.parametrize('page_num', reversed(range(1, 11)))
    def test_page_data_with_next_previous_navigation(self, open_website, page_num, page: Page) -> None:
        members_table = MembersTablePage(page)
        if page_num != 10:
            members_table.insert_page(page_num + 1)
            members_table.click_previous_button()
        else:
            members_table.insert_page(page_num)
        assert members_table.get_current_page_number() == page_num, 'page number didn\'t changed'
        table_from_api = members_table.get_table_from_api(page_num)
        table_from_ui = members_table.get_table_data()
        assert table_from_ui == table_from_api, 'the data in the table in page ' + str(
            page_num) + 'is not equal to the API data'

    def test_insert_non_existing_page(self, open_website, page: Page) -> None:
        members_table = MembersTablePage(page)
        members_table.insert_page(random.randint(11, 999))
        table_from_ui = members_table.get_table_data()
        assert not any(table_from_ui), 'the non exsiting page present data'

    def test_insert_invalid_page(self, open_website, page: Page) -> None:
        members_table = MembersTablePage(page)
        table_from_ui_before_invalid_data = members_table.get_table_data()
        members_table.insert_page('hasghgsa')
        table_from_ui_after_invalid_data = members_table.get_table_data()
        assert table_from_ui_before_invalid_data == table_from_ui_after_invalid_data, 'the invalid input affected present data'