from dataclasses import dataclass
from pathlib import Path

from rithm.tasks.task import Task


@dataclass
class TestTask:
    target: Path
    profile: str


class TestTaskParser:
    type = "test"

    def parse(self, task: Task):
        tests = task[self.type]
        return [
            TestTask(
                task.directory / test["target"],
                test["profile"],
            )
            for test in tests
        ]
