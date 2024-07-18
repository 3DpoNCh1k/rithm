from dataclasses import dataclass
from pathlib import Path

from rithm.tasks.task import Task


@dataclass
class ExampleTask:
    examples: Path
    solution: Path
    profile: str


class ExampleTaskParser:
    type = "examples"

    def can_parse(self, task: Task):
        return self.type in task

    def parse(self, task: Task):
        targets = task[self.type]
        return [
            ExampleTask(
                task.directory / "examples",
                task.directory / target["solution"],
                target["profile"],
            )
            for target in targets
        ]
