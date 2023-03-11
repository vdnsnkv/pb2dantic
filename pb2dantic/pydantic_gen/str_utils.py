def is_camel_case(s: str):
    return any([ch.isupper() for ch in s])


def snake_case(s: str):
    return s[0] + "".join(["_" + ch if ch.isupper() else ch for ch in s[1:]]).lower()
