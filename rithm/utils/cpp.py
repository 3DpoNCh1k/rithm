import re


def remove_pragma_once(text):
    return re.sub("#pragma once", "", text).lstrip()


def remove_includes(text):
    new_text_parts = []
    last_index = 0
    for match in re.finditer(r"(?P<include>#include.*\n?)", text):
        new_text_parts.append(text[last_index : match.start()])
        last_index = match.end()

    new_text_parts.append(text[last_index:])
    new_text = "".join(new_text_parts)
    new_text = new_text.lstrip()
    return new_text


def generate_includes(dependencies):
    include_list = list(map(lambda name: f"#include <{name}>", dependencies))
    include_text = "\n".join(include_list)
    return include_text


def has_pragma_once(path):
    return path.open().read().startswith("#pragma once")
