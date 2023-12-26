from bs4 import BeautifulSoup

from text_utils import substring_from_text_html, get_value_from_substring, exclude_substring, substring_with_regex
from cast_utils import cast_float, cast_int


class SoupHelper:

    def __init__(self, html, parser='html.parser'):
        self.soup = BeautifulSoup(html, parser)
        self.separator_value = ":"

    def get_value_by_selector_and_name(self, selector: str, name: str) -> str | None:
        tag = self.soup.select_one(selector)
        if tag is None:
            return None
        text = tag.get_text()
        substring = substring_from_text_html(name, text)
        return get_value_from_substring(substring, self.separator_value, 1)

    def get_value_by_selector_and_exclude_substring(self, selector: str, name: str, substring: str) -> str:
        value = self.get_value_by_selector_and_name(selector, name)
        return exclude_substring(substring, value)

    def get_substring_value_by_selector(self, selector: str) -> str | None:
        tag = self.soup.select_one(selector)
        if tag is None:
            return None
        text = tag.get_text()
        return get_value_from_substring(text, self.separator_value)

    def get_value_attr_by_selector(self, selector: str, name_attr: str) -> str | None:
        tag = self.soup.select_one(selector)
        if tag is None:
            return None
        return tag[name_attr]

    def parse_value_by_selector(self, selector: str, parse_func) -> str | None:
        tag = self.soup.select_one(selector)
        if tag is None:
            return None
        text = tag.get_text()
        return parse_func(text)

    def get_elements_by_selector(self, selector: str) -> list:
        tags = self.soup.select(selector)
        return list(tags)

    def get_value_by_selector(self, selector: str) -> str | None:
        tag = self.soup.select_one(selector)
        if tag is None:
            return None
        return tag.get_text().strip()

    def get_num_value_by_selector(self, selector: str) -> int | None:
        return cast_int(self.parse_value_by_selector(selector, lambda raw: substring_with_regex(raw, r'-?\d+')))

    def get_float_num_value_by_selector(self, selector: str) -> float | None:
        pattern = r'[-+]?([0-9]*\.[0-9]+|[0-9]+)'
        return cast_float(self.parse_value_by_selector(selector, lambda raw: substring_with_regex(raw, pattern)))
