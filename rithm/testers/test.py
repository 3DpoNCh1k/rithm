import tempfile
from pathlib import Path

from rithm.staff.builder import Builder
from rithm.staff.runner import Runner
from rithm.tasks.test import TestTask


class Tester:
    task_type = TestTask

    def __init__(self, builder):
        self.builder = builder
        self.runner = Runner()

    def test(self, task: TestTask, _testcase=None):
        with tempfile.TemporaryDirectory() as directory:
            target_executable = Path(directory) / "target"
            self.builder.build(task.profile, task.target, target_executable)
            self.runner.run(target_executable)
