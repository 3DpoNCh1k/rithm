from rithm.graph import create_graph, get_algo_name, get_topological_order
from rithm.source_files import CppFile, File

from .tasks.codeforces import CodeforcesTaskParser
from .tasks.library_checker import LibraryCheckerTaskParser
from .tasks.task import Task
from .tasks.test import TestTaskParser
from .utils import *


class Algo:
    def __init__(self, path: Path):
        self.path = path
        self.task_parsers = [
            LibraryCheckerTaskParser(),
            CodeforcesTaskParser(),
            TestTaskParser(),
        ]

    @property
    def source_code_path(self):
        return self.path / "algo"

    @property
    def tests_path(self):
        return self.path / "tests"

    def get_all_tasks(self, search_path, task_type):
        tasks_list = map(self.get_tasks, search_path.glob("**/task.json"))
        tasks = [task for tasks in tasks_list for task in tasks]
        if task_type is not None:
            tasks = filter(lambda task: isinstance(task, task_type), tasks)
        return list(tasks)

    def get_tasks(self, path):
        task = Task(path)
        tasks = []
        for parser in self.task_parsers:
            if parser.type in task:
                tasks += parser.parse(task)
        return tasks

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

    def check_include_all(self):
        include_all_file = self.tests_path / "include_all.cpp"
        include_all_filenames = set(CppFile(include_all_file).algo_dependencies)
        algo_filenames = set(
            map(
                get_algo_name,
                get_files_from_directory(self.source_code_path, recursive=True),
            )
        )

        if algo_filenames != include_all_filenames:
            not_included = algo_filenames - include_all_filenames
            not_exist = include_all_filenames - algo_filenames
            if not_included:
                print(f"Files that are not included: {sorted(not_included)}")
            if not_exist:
                print(f"Files that does not exist: {sorted(not_exist)}")

    def generate_include_all(self, filenames):
        return "\n".join(f"#include <{name}>" for name in sorted(filenames))

    def check_extensions(self):
        consistent_extension = "hpp"
        for file in get_files_from_directory(self.source_code_path, recursive=True):
            if File(file).extension != consistent_extension:
                print(f'{file} is not a "{consistent_extension}" file')
                sys.exit(1)
