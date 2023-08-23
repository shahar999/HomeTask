from Base.BasePage import BasePage
from Base.API import API

class MembersTablePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.next_button = 'data-testid=ArrowRightIcon'
        self.previous_button = 'data-testid=ArrowLeftIcon'
        self.page_input = 'id=:r0:'
        self.api_get_page = 'http://localhost:5000/page?page='
        self.table_rows = "//*[@class='MuiTableRow-root css-1gqug66']"
        self.table_heads = "//*[@class='MuiTableRow-root MuiTableRow-head css-1gqug66']/th"

    def get_table_from_api(self, page_num):
        return API.get_request(self.api_get_page + str(page_num))

    def get_last_record_page_from_api(self):
        page_num = 10
        while page_num < 100:
            if self.get_table_from_api(1) == self.get_table_from_api(page_num):
                break
            page_num += 1
        return page_num - 1

    def get_page_last_record_api(self):
        return self.get_table_from_api(self.get_last_record_page_from_api())[-1]

    def get_number_of_members_api(self):
        return self.get_last_record_page_from_api() * 10 - (10 - len(self.get_table_from_api(self.get_last_record_page_from_api())))

    def navigate_to_table(self):
        self.navigate("http://localhost:3000/")

    def click_next_button(self):
        self.click(self.get_element(self.next_button))

    def click_previous_button(self):
        self.click(self.get_element(self.previous_button))

    def insert_page(self, page_num):
        self.insert_text(self.get_element(self.page_input), str(page_num))
        self.page.keyboard.press('Enter')

    def get_table_data(self):
        table_data = []
        table_head_text = self.get_locator_texts(self.table_heads)
        for i in range(1, len(self.get_elements(self.table_rows)) + 1):
            row_cells_text = self.get_locator_texts(self.table_rows + "[" + str(i) + "]/td")
            row_data = {}
            for j in range(len(table_head_text)):
                row_data.update({str.lower(table_head_text[j]) : row_cells_text[j]})
            row_data['id'] = int(row_data['id'])
            table_data.append(row_data)
        return table_data

    def get_current_page_number(self):
        return int(self.get_input_value(self.get_element(self.page_input)))
