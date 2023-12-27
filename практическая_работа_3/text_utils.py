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
    if substring is None or len(substring) == 0:
        return None
    arr = substring.split(separator)
    if len(arr) > 0:
        return arr[index_element].strip()
    return None


def get_value_from_substring_with_exclude(substring: str, separator: str,
                                          exclude: str, index_element: int = -1) -> str | None:
    value = get_value_from_substring(substring, separator, index_element)
    if value is None:
        return None
    return exclude_substring(exclude, value)

def substring_with_regex(text: str, pattern: str, exclude: str = None, index: int = 0) -> str | None:
    if text is None:
        return None
    match_list = re.findall(pattern, text)
    if match_list is None or len(match_list) == 0:
        return None
    value = match_list[index]
    if exclude is not None:
        return value.replace(exclude, '').strip()
    return value
