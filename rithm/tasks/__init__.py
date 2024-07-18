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


def _get_parsers(task_type):
    parsers = [
        LibraryCheckerTaskParser(),
        CodeforcesTaskParser(),
        TestTaskParser(),
    ]
    if task_type is None:
        return parsers
    return list(filter(lambda parser: parser.type == task_type, parsers))


def get_all_tasks(search_path, task_type=None):
    tasks_list = map(
        lambda path: get_tasks(path, task_type),
        search_path.glob("**/task.json"),
    )
    return [task for tasks in tasks_list for task in tasks]


def get_tasks(path, task_type=None):
    task = Task(path)
    tasks = []
    parsers = _get_parsers(task_type)
    assert any([p.can_parse(task) for p in parsers])
    for parser in parsers:
        if parser.can_parse(task):
            tasks += parser.parse(task)
    return tasks
