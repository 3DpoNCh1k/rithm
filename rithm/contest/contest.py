import os
import shutil
from pathlib import Path

from rithm.utils import get_files_from_directory

CONTEST_DIRECTORY = Path(os.path.realpath(__file__)).parent


class Contest:
    def __init__(self):
        pass

    def create_problems(self, problems: list[str]):
        for problem in problems:
            self.create_problem(problem)

    def create_problem(self, problem: str):
        current_path = Path(".")
        problem_path = current_path / problem
        examples_path = problem_path / "examples"
        inputs_path = examples_path / "inputs"
        outputs_path = examples_path / "outputs"
        problem_path.mkdir()
        examples_path.mkdir()
        inputs_path.mkdir()
        outputs_path.mkdir()

        for file in get_files_from_directory(self.templates_path):
            shutil.copy(file, problem_path)

    @property
    def templates_path(self):
        return CONTEST_DIRECTORY / "templates"
