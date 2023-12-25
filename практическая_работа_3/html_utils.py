from bs4 import BeautifulSoup
from text_utils import substring_from_text_html, get_value_from_substring, exclude_substring


class SoupHelper:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.separator_value = ":"

    def get_value_by_selector_and_name(self, selector: str, name: str) -> str:
        text = self.soup.select_one(selector).get_text()
        substring = substring_from_text_html(name, text)
        return get_value_from_substring(substring, self.separator_value, 1)

    def get_value_by_selector_and_exclude_substring(self, selector: str, name: str, substring: str) -> str:
        value = self.get_value_by_selector_and_name(selector, name)
        return exclude_substring(substring, value)

    def get_value_by_selector(self, selector: str) -> str:
        text = self.soup.select_one(selector).get_text()
        return get_value_from_substring(text, self.separator_value)

    def get_value_attr_by_selector(self, selector: str, name_attr: str) -> str:
        return self.soup.select_one(selector)[name_attr]
