import re

PATTERN = re.compile(r"([0-9]+)([kmbtq])([0-9]*)")

CONVERSIONS = {
    "k": "1000",
    "m": "1000000",
    "B": "1000000000",
    "T": "1000000000000",
    "Q": "1000000000000000",
}


def sub_fn(match):
    if match.group(3):
        return "({0} * {1} + {2})".format(
            match.group(1), CONVERSIONS[match.group(2)], match.group(3)
        )
    else:
        return "({0} * {1})".format(match.group(1), CONVERSIONS[match.group(2)])


def convert(text):
    return re.sub(PATTERN, sub_fn, text)
