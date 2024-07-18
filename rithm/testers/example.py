import tempfile
from pathlib import Path

from rithm.staff import ExamplesRunner
from rithm.staff.builder import Builder
from rithm.tasks.example import ExampleTask


class ExampleTester:
    task_type = ExampleTask

    def __init__(self, builder: Builder):
        self.builder = builder
        self.runner = ExamplesRunner()

    def test(self, task: ExampleTask, _testcase=None):
        with tempfile.TemporaryDirectory() as directory:
            solution_executable = Path(directory) / "solution"
            self.builder.build(task.profile, task.solution, solution_executable)
            self.runner.run(solution_executable, task.examples)
