import re
import subprocess
from pathlib import Path


class LibraryChecker:
    def __init__(self, path: Path):
        assert path.is_absolute()
        self.path = path

    @property
    def generator(self):
        return self.path / "generate.py"

    def create_problem_checker(self, path):
        return ProblemChecker(self, path)


class ProblemChecker:
    def __init__(self, library_checker: LibraryChecker, problem: Path):
        assert not problem.is_absolute()
        self.library_checker = library_checker
        self.path = problem
        assert self.absolute_path.exists()

    def generate_testcases(self):
        test_info = self.absolute_path / "info.toml"
        cmd = f"{self.library_checker.generator} {test_info}"
        subprocess.check_call(cmd, shell=True)

    def get_testcases(self):
        return sorted(map(lambda path: path.name, self.testcases_path.glob("*.in")))

    def validate_testcase(self, testcase: str, output: Path):
        correct_output = self.corresponding_answer(testcase)
        cmd = f"{self.checker} {self.testcase_path(testcase)} {output} {correct_output}"
        print(f"Validating {testcase}")
        subprocess.check_call(cmd, shell=True)

    def validate_testcases(self, outputs: Path):
        for testcase in self.get_testcases():
            self.validate_testcase(
                testcase, self.corresponding_output(outputs, testcase)
            )

    @property
    def absolute_path(self):
        return self.library_checker.path / self.path

    @property
    def testcases_path(self):
        return self.absolute_path / "in"

    @property
    def answers_path(self):
        return self.absolute_path / "out"

    @property
    def checker(self):
        return self.absolute_path / "checker"

    def testcase_path(self, testcase: str):
        return self.testcases_path / testcase

    def corresponding_answer(self, testcase: str):
        return self.corresponding_output(self.answers_path, testcase)

    def corresponding_output(self, outputs: Path, testcase: str):
        name = re.match(r"(?P<name>.*)\.in", testcase).group("name")
        return outputs / f"{name}.out"
