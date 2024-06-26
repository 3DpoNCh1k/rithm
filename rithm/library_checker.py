from pathlib import Path
import subprocess


class ProblemChecker:
    def __init__(self, library_checker, problem_path: Path):
        assert not problem_path.is_absolute()
        self.library_checker = library_checker
        self.path = problem_path
        assert self.absolute_path.exists()

    def generate_testcases(self):
        test_info = self.absolute_path / "info.toml"
        cmd = f"{self.library_checker.generator} {test_info}"
        subprocess.check_call(cmd, shell=True)

    def get_testcases(self):
        return sorted(self.testcases_path.glob("*.in"))

    def validate_testcase(self, testcase, output):
        correct_output = self.corresponding_answer(testcase)
        cmd = f"{self.checker} {testcase} {output} {correct_output}"
        print(f"Validation {testcase.name}")
        subprocess.check_call(cmd, shell=True)

    def validate_testcases(self, outputs_path, testcase=None):
        testcases = self.get_testcases()
        if testcase is not None:
            testcases = list(filter(lambda path: path.name == testcase, testcases))
        for testcase in testcases:
            self.validate_testcase(
                testcase, self.corresponding_output(outputs_path, testcase)
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

    def corresponding_answer(self, testcase):
        return self.corresponding_output(self.answers_path, testcase)

    def corresponding_output(self, outputs_path, testcase):
        name = testcase.name[:-3]
        return outputs_path / f"{name}.out"


class LibraryChecker:
    def __init__(self, path: Path):
        assert path.is_absolute()
        self.path = path

    @property
    def generator(self):
        return self.path / "generate.py"

    def create_problem_checker(self, path):
        return ProblemChecker(self, path)
