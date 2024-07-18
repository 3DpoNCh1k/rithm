from .codeforces import *
from .example import *
from .library_checker import *
from .task import *
from .test import *

__all__ = [
    "Task",
    "CodeforcesTask",
    "LibraryCheckerTask",
    "TestTask",
    "ExampleTask",
    "get_all_tasks",
    "get_tasks",
]


def _get_parsers(task_type):
    parsers = [
        LibraryCheckerTaskParser(),
        CodeforcesTaskParser(),
        TestTaskParser(),
        ExampleTaskParser(),
    ]
    if task_type is None:
        return parsers
    return list(filter(lambda parser: parser.type == task_type, parsers))


def get_all_tasks(search_path, task_type=None):
    tasks = []
    for path in sorted(search_path.glob("**/task.json")):
        tasks.extend(get_tasks(path, task_type))
    return tasks


def get_tasks(path, task_type=None):
    print(path)
    task = Task(path)
    tasks = []
    parsers = _get_parsers(task_type)
    for parser in parsers:
        if parser.can_parse(task):
            tasks += parser.parse(task)
    return tasks
