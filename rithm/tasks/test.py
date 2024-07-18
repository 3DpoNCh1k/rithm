from dataclasses import dataclass
from pathlib import Path

from rithm.tasks.task import Task


@dataclass
class TestTask:
    target: Path
    profile: str


class TestTaskParser:
    type = "tests"

    def can_parse(self, task: Task):
        return self.type in task

    def parse(self, task: Task):
        tests = task[self.type]
        return [
            TestTask(
                task.directory / test["target"],
                test["profile"],
            )
            for test in tests
        ]
