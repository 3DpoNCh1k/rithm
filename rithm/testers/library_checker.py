import tempfile
from pathlib import Path

from rithm.staff.builder import Builder
from rithm.staff.library_checker import LibraryChecker
from rithm.staff.runner import Runner
from rithm.tasks.library_checker import LibraryCheckerTask


class LibraryCheckerTester:
    task_type = LibraryCheckerTask

    def __init__(self, builder: Builder, library_checker: LibraryChecker):
        self.builder = builder
        self.runner = Runner()
        self.library_checker = library_checker

    def test(self, task: LibraryCheckerTask, testcase=None):
        problem_checker = self.library_checker.create_problem_checker(task.problem)
        problem_checker.generate_testcases()

        with tempfile.TemporaryDirectory() as directory:
            solution_executable = Path(directory) / "solution"
            self.builder.build(task.profile, task.solution, solution_executable)
            testcases = (
                [testcase] if testcase is not None else problem_checker.get_testcases()
            )
            for testcase in testcases:
                testcase_path = problem_checker.testcase_path(testcase)
                output_path = Path(directory) / "output"
                self.runner.run(
                    solution_executable, testcase_path.open(), output_path.open("w")
                )
                problem_checker.validate_testcase(testcase, output_path)
