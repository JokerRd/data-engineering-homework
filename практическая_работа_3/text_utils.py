import re


def substring_from_text_html(name: str, text: str) -> str | None:
    pattern = r'' + name + '.*' + ':' + '.*'
    match = re.search(pattern, text)
    if match is not None:
        return match.group()
    return None


def exclude_substring(substring: str, text: str) -> str | None:
    return text.replace(substring, '').strip()

def get_value_from_substring(substring: str, separator: str, index_element: int = -1) -> str | None:
    arr = substring.split(separator)
    if len(arr) > 0:
        return arr[index_element].strip()
    return None