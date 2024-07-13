from dataclasses import dataclass
from pathlib import Path

from rithm.tasks.task import Task


@dataclass
class LibraryCheckerTask:
    link: str
    problem: Path
    solution: Path
    profile: str


class LibraryCheckerTaskParser:
    type = "library-checker"

    def parse(self, task: Task):
        problem = task[self.type]
        return [
            LibraryCheckerTask(
                problem["link"],
                Path(problem["path"]),
                task.directory / target["solution"],
                target["profile"],
            )
            for target in problem["targets"]
        ]
