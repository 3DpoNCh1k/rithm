from dataclasses import dataclass
from pathlib import Path

from rithm.tasks.task import Task


@dataclass
class CodeforcesTask:
    link: str
    solution: Path


class CodeforcesTaskParser:
    type = "codeforces"

    def parse(self, task: Task):
        problem = task[self.type]
        return [CodeforcesTask(problem["link"], task.directory / problem["solution"])]
