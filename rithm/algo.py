import json

from rithm.graph import create_graph, get_topological_order

from .utils import *


class Task:
    def __init__(self, path):
        self._path = path
        self._content = json.load(path.open())

    def __getitem__(self, key):
        return self._content.get(key)

    def __repr__(self):
        return str(self._path)

    def has_library_checker_tests(self):
        return "library-checker-problems" in self._content

    def has_solution(self):
        return "solution" in self._content

    def has_local_tests(self):
        return "target" in self._content

    def has_link(self):
        return "link" in self._content

    @property
    def solution_path(self):
        return self._path.parent / self._content["solution"]

    @property
    def target_path(self):
        return self._path.parent / self._content["target"]


class Algo:
    def __init__(self, path):
        self.path = path

    def get_all_tasks(self, search_path):
        return list(map(lambda path: Task(path), search_path.glob("**/task.json")))

    def get_task(self, path):
        return Task(path)

    def expand_includes(self, text, dependency_order):
        algo_text_list = []
        for file_node in dependency_order:
            file_text = file_node.file.text
            file_text = remove_pragma(file_text)
            file_text = remove_includes(file_text)
            algo_text_list.append(file_text)

        algo_text = "\n".join(algo_text_list)
        return text + "\n" + algo_text

    def create_submission_text(self, file_path):
        dependency_graph = create_graph(file_path)
        dependency_order = get_topological_order(dependency_graph)
        std_dependencies = set()
        for file_node in dependency_order:
            std_dependencies.update(file_node.file.std_dependencies)

        header = "// TODO: add header"
        text = header
        text = add_std_includes(text, std_dependencies)
        text = self.expand_includes(text, dependency_order)

        return text
