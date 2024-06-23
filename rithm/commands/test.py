import json
import os
from pathlib import Path
import subprocess
import sys

# TODO: handle it better
try:
    ALGO_PATH = Path(os.environ['ALGO_PATH'])
except KeyError:
    print("Set ALGO_PATH environment variable that points to algo library")
    sys.exit(1)

COMMANDS_DIRECTORY = Path(os.path.realpath(__file__)).parent
RITHM_DIRECTORY = COMMANDS_DIRECTORY.parent.parent
LIBRARY_CHECKER_DIRECTORY = RITHM_DIRECTORY / "library-checker-problems"


class Task:
    def __init__(self, path):
        self._path = path
        self._content = json.load(path.open())
    
    def __getitem__(self, key):
        return self._content.get(key)
    
    def __repr__(self):
        return str(self._path)
    
    def has_local_tests(self):
        return "library-checker-problems" in self._content

    def has_solution(self):
        return "solution" in self._content
    
    @property
    def solution_path(self):
        return self._path.parent / self._content["solution"]

def get_all_tasks(path):
    return list(map(lambda path: Task(path), path.glob("**/task.json")))

def process_task(task: Task):
    if task.has_local_tests() and task.has_solution():
        test_task(task)

def compile_solver(solution_path, solver_path):
    cmd = f"g++ --std=c++17 -I {ALGO_PATH} -Wall -Wextra -Wshadow -fsanitize=address -fsanitize=undefined -o {solver_path} {solution_path}"
    subprocess.check_call(cmd, shell=True)

def test_task(task: Task):
    checker_path = Path(LIBRARY_CHECKER_DIRECTORY / task["library-checker-problems"])
    generate_testcases(checker_path)
    tmp_rithm_path = Path("/tmp/rithm")
    tmp_rithm_path.mkdir(exist_ok=True) 
    outputs_path = tmp_rithm_path / "outputs"
    outputs_path.mkdir(exist_ok=True)
    solver_path = tmp_rithm_path / "solver.exe"
    compile_solver(task.solution_path, solver_path)
    produce_solution_outputs(solver_path, checker_path, outputs_path)
    validate_solution_outputs(checker_path, outputs_path)

def generate_testcases(checker_path):
    generator = LIBRARY_CHECKER_DIRECTORY / "generate.py"
    test_info = checker_path / "info.toml"
    cmd = f"{generator} {test_info}"
    subprocess.check_call(cmd, shell=True)

def validate_output(checker_path, input, my, correct):
    checker = checker_path / "checker"
    cmd = f"{checker} {input} {my} {correct}"
    print(f"Validation {input.name}")
    subprocess.check_call(cmd, shell=True)

def validate_solution_outputs(checker_path, output_path):
    print("validate_solution_outputs")
    testcases_path = checker_path / "in"
    answers_path = checker_path / "out"
    for testcase in sorted(testcases_path.glob("*.in")):
        name = testcase.name[:-3]
        my_output = output_path / f"{name}.out"
        correct_output = answers_path / f"{name}.out"
        validate_output(checker_path, testcase, my_output, correct_output)

def produce_solution_outputs(solution_path, checker_path, output_path):
    print("produce_solution_outputs")
    testcases_path = checker_path / "in"
    answers_path = checker_path / "out"
    for testcase in sorted(testcases_path.glob("*.in")):
        name = testcase.name[:-3]
        my_output = output_path / f"{name}.out"
        produce_solution_output(solution_path, testcase, my_output)

def produce_solution_output(solution_path, testcase_path, output_path):
    cmd = f"{solution_path} < {testcase_path} > {output_path}"
    subprocess.check_call(cmd, shell=True)

def test_command(args):
    path = Path(args.path)
    tasks = get_all_tasks(path)
    for task in tasks:
        process_task(task)