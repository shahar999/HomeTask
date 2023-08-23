import string
import random
import pytest
from playwright.sync_api import Page, expect, sync_playwright
from pages.MembersTablePage import MembersTablePage
from pages.AddMemberPage import AddMemberPage

letters = string.ascii_letters

class TestAddMember:
    @pytest.fixture()
    def open_add_member_window(self, page: Page):
        add_members = AddMemberPage(page)
        add_members.open_add_new_member_window()

    def test_add_member(self, open_add_member_window, page: Page):
        members_table = MembersTablePage(page)
        add_members = AddMemberPage(page)
        member = {}
        member.update({'name': ''.join(random.choice(letters) for i in range(10))})
        member.update({'family': ''.join(random.choice(letters) for i in range(10))})
        member.update({'id': members_table.get_number_of_members_api()})
        add_members.insert_name(member['name'])
        add_members.insert_family(member['family'])
        add_members.click_add_member()
        assert members_table.get_page_last_record_api() == member, 'new member data is not correct'

    def test_add_member_with_invalid_data(self, open_add_member_window, page: Page):
        members_table = MembersTablePage(page)
        add_members = AddMemberPage(page)
        member = {}
        member.update({'name': '$%#$%#$%^'})
        member.update({'family': '$%#$%#$%^'})
        member.update({'id': members_table.get_number_of_members_api()})
        add_members.insert_name(member['name'])
        add_members.insert_family(member['family'])
        add_members.click_add_member()
        last_record = members_table.get_page_last_record_api()
        assert last_record['name'] != '$%#$%#$%^' and last_record['family'] != '$%#$%#$%^', 'member with invalid data was added'

    def test_add_member_with_empty_data(self, open_add_member_window, page: Page):
        members_table = MembersTablePage(page)
        add_members = AddMemberPage(page)
        add_members.click_add_member()
        last_record = members_table.get_page_last_record_api()
        assert last_record['name'] != '' and last_record['family'] != '', 'member with empty data was added'

    def test_add_existing_member(self, open_add_member_window, page: Page):
        members_table = MembersTablePage(page)
        add_members = AddMemberPage(page)
        member = {}
        member.update({'name': ''.join(random.choice(letters) for i in range(10))})
        member.update({'family': ''.join(random.choice(letters) for i in range(10))})
        member.update({'id': members_table.get_number_of_members_api()})
        add_members.insert_name(member['name'])
        add_members.insert_family(member['family'])
        add_members.click_add_member()
        first_added_member = members_table.get_page_last_record_api()
        add_members.open_add_new_member_window()
        add_members.insert_name(member['name'])
        add_members.insert_family(member['family'])
        add_members.click_add_member()
        last_record = members_table.get_page_last_record_api()
        assert first_added_member != last_record, 'duplicate member was accepted'
