from pathlib import Path
import re

from rithm.graph import *
from rithm.source_files import *


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


def expand_algo_includes(text, dependency_order):
    algo_text_list = []
    for file_node in dependency_order:
        file_text = file_node.file.text
        file_text = remove_pragma(file_text)
        file_text = remove_includes(file_text)
        algo_text_list.append(file_text)

    algo_text = "\n".join(algo_text_list)
    return text + "\n" + algo_text


def prepare_submission_command(args):
    filename = args.filename
    file_path = Path(filename)
    folder = file_path.parent

    dependency_graph = create_graph(file_path)
    dependency_order = get_topological_order(dependency_graph)
    std_dependencies = set()
    for file_node in dependency_order:
        std_dependencies.update(file_node.file.std_dependencies)

    header = "// TODO: add header"
    text = header
    text = add_std_includes(text, std_dependencies)
    text = expand_algo_includes(text, dependency_order)

    submission_text = text
    name = file_path.name
    new_folder_path = Path(".") / "submit" / folder.name
    new_folder_path.mkdir(parents=True, exist_ok=True)
    open(new_folder_path / f"submission_{name}", "w").write(submission_text)
