from rithm.graph import create_graph, get_topological_order

from .task import *
from .utils import *


class Algo:
    def __init__(self, path):
        self.path = path

    def get_all_tasks(self, search_path):
        return list(map(self.get_task, search_path.glob("**/task.json")))

    def get_task(self, path):
        task = Task(path)
        if "library-checker-problems" in task and "solution" in task:
            return LibraryCheckerTask(
                task["link"],
                Path(task["library-checker-problems"]),
                task.directory / task["solution"],
            )
        if "target" in task:
            return TestTask(task.directory / task["target"])
        if (
            "link" in task
            and task["link"].startswith("https://codeforces.com")
            and "solution" in task
        ):
            return CodeforcesTask(task["link"], task.directory / task["solution"])

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
