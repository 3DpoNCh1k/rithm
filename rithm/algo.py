import json
from .utils import *


class Task:
    def __init__(self, path):
        self._path = path
        self._content = json.load(path.open())

    def __getitem__(self, key):
        return self._content.get(key)

    def __repr__(self):
        return str(self._path)

    def has_local_tests(self):
        return "library-checker-problems" in self._content

    def has_solution(self):
        return "solution" in self._content

    @property
    def solution_path(self):
        return self._path.parent / self._content["solution"]


class Algo:
    def __init__(self, path):
        self.path = path

    def get_all_tasks(self, search_path):
        return list(map(lambda path: Task(path), search_path.glob("**/task.json")))

    def expand_algo_includes(self, text, dependency_order):
        algo_text_list = []
        for file_node in dependency_order:
            file_text = file_node.file.text
            file_text = remove_pragma(file_text)
            file_text = remove_includes(file_text)
            algo_text_list.append(file_text)

        algo_text = "\n".join(algo_text_list)
        return text + "\n" + algo_text
