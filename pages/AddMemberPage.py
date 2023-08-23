from Base.BasePage import BasePage


class AddMemberPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_member_open_window = 'data-testid=PersonAddIcon'
        self.name_input = 'id=:r1:'
        self.family_input = 'id=:r2:'
        self.add_button = "//button[text()='Add']"

    def open_add_new_member_window(self):
        self.navigate("http://localhost:3000/")
        self.click(self.get_element(self.add_member_open_window))

    def click_add_member(self):
        self.click(self.get_element(self.add_button))

    def insert_name(self, name):
        self.insert_text(self.get_element(self.name_input), name)

    def insert_family(self, family):
        self.insert_text(self.get_element(self.family_input), family)
