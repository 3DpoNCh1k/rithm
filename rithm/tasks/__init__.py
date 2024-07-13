from .codeforces import *
from .library_checker import *
from .task import *
from .test import *

__all__ = [
    "Task",
    "CodeforcesTask",
    "LibraryCheckerTask",
    "TestTask",
    "get_all_tasks",
    "get_tasks",
]


def _get_parsers(type):
    parsers = [
        LibraryCheckerTaskParser(),
        CodeforcesTaskParser(),
        TestTaskParser(),
    ]
    if type is None:
        return parsers
    list(filter(lambda parser: parser.type == type))


def get_all_tasks(self, search_path, task_type=None):
    tasks_list = map(
        lambda path: self.get_tasks(path, task_type),
        search_path.glob("**/task.json"),
    )
    return [task for tasks in tasks_list for task in tasks]


def get_tasks(self, path, task_type=None):
    task = Task(path)
    tasks = []
    for parser in _get_parsers(task_type):
        tasks += parser.parse(task)
    return tasks
