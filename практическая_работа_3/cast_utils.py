def cast_from_str_to(text: str, cast_func):
    if text is None or len(text) == 0:
        return None
    return cast_func(text)


def cast_int(text: str) -> int | None:
    return cast_from_str_to(text, lambda string: int(string.replace(' ', '')))


def cast_float(text: str) -> int | None:
    return cast_from_str_to(text, lambda string: float(string.replace(' ', '')))
