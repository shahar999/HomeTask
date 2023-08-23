class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, element):
        element.click()

    def get_element(self, locator):
        return self.page.locator(locator)

    def insert_text(self, element, text):
        element.fill(text)

    def get_locator_texts(self, locator):
        return self.page.locator(locator).all_inner_texts()

    def get_elements(self, elements):
        return self.page.locator(elements).all()

    def get_input_value(self, element):
        return element.input_value()