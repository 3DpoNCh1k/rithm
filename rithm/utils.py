import re


def remove_pragma(text):
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


def add_std_includes(text, std_dependencies):
    include_list = list(map(lambda name: f"#include <{name}>", std_dependencies))
    include_text = "\n".join(include_list)
    return text + "\n" + include_text


def has_pragma(path):
    return path.open().read().startswith("#pragma once")
