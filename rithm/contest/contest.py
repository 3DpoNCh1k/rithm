import os
from pathlib import Path

CONTEST_DIRECTORY = Path(os.path.realpath(__file__)).parent


class Contest:
    def __init__(self):
        template_path = CONTEST_DIRECTORY / "template.cpp"
        self.main_template = template_path.open().read()

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
        main_program_path = problem_path / "main.cpp"
        main_program_path.open("w").write(self.main_template)
