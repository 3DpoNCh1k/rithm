import os
import subprocess
from pathlib import Path
import re

import json
import os
from pathlib import Path
import subprocess
import sys



from .config import load_config

from .graph import *
from .source_files import *


# TODO: handle it better
try:
    ALGO_PATH = Path(os.environ["ALGO_PATH"])
except KeyError:
    print("Set ALGO_PATH environment variable that points to algo library")
    sys.exit(1)

COMMANDS_DIRECTORY = Path(os.path.realpath(__file__)).parent
RITHM_DIRECTORY = COMMANDS_DIRECTORY.parent.parent
LIBRARY_CHECKER_DIRECTORY = RITHM_DIRECTORY / "library-checker-problems"



def remove_pragma(text):
    return re.sub("#pragma once", "", text).lstrip()


def remove_includes(text):
    new_text_parts = []
    last_index = 0
    for match in re.finditer(r"(?P<include>#include.*\n?)", text):
        new_text_parts.append(text[last_index : match.start()])
        last_index = match.end()

    new_text_parts.append(text[last_index:])
    new_text = "".join(new_text_parts)
    new_text = new_text.lstrip()
    return new_text


def add_std_includes(text, std_dependencies):
    include_list = list(map(lambda name: f"#include <{name}>", std_dependencies))
    include_text = "\n".join(include_list)
    return text + "\n" + include_text


def expand_algo_includes(text, dependency_order):
    algo_text_list = []
    for file_node in dependency_order:
        file_text = file_node.file.text
        file_text = remove_pragma(file_text)
        file_text = remove_includes(file_text)
        algo_text_list.append(file_text)

    algo_text = "\n".join(algo_text_list)
    return text + "\n" + algo_text



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




def has_pragma(path):
    return path.open().read().startswith("#pragma once")


def check_pragma(path):
    header_extensions = ["hpp", "h"]
    for ext in header_extensions:
        for file_path in path.glob(f"**/*.{ext}"):
            if not has_pragma(file_path):
                print(f"File {file_path} does not has #pragma once")
                sys.exit(1)

    print("Success!")







class Rithm:
    def run_command(self, profile, compiler, filename, local_debug):
        print("Rithm.run_command")
        return

        executable = filename[:-4] + ".exe"

        config = load_config()
        config = config["compiler"][compiler]
        std = config["std"]
        always_flags = config["always"]
        profile_flags = config["profiles"][profile]
        debug_flags = config["localDebug"] if local_debug else ""

        cmd = f"{compiler} --std={std} {always_flags} {profile_flags} {debug_flags}"
        cmd += f" -o {executable} {filename}"

        if os.path.exists(executable):
            os.remove(executable)

        res = subprocess.run(cmd, shell=True, check=True)
        assert res.returncode == 0
        res = subprocess.run(executable, shell=True, check=True)
        assert res.returncode == 0

    def prepare_submission_command(self, filename):
        file_path = Path(filename)
        print("Rithm.prepare_submission_command")
        return
    
        folder = file_path.parent

        dependency_graph = create_graph(file_path)
        dependency_order = get_topological_order(dependency_graph)
        std_dependencies = set()
        for file_node in dependency_order:
            std_dependencies.update(file_node.file.std_dependencies)

        header = "// TODO: add header"
        text = header
        text = add_std_includes(text, std_dependencies)
        text = expand_algo_includes(text, dependency_order)

        submission_text = text
        name = file_path.name
        new_folder_path = Path(".") / "submit" / folder.name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        open(new_folder_path / f"submission_{name}", "w").write(submission_text)
    
    def test_command(self, path):
        print("Rithm.test_command")
        return
        path = Path(path)
        tasks = get_all_tasks(path)
        for task in tasks:
            process_task(task)
    
    def clean_command(self, path):
        print("Rithm.clean_command")
        return
        path = args.path
        patterns = [".*\.exe$", ".*\.exp$", ".*\.lib$", ".*\.pdb$"]
        for path, _, filenames in os.walk(path):
            to_remove = filter(
                lambda filename: any(re.match(pattern, filename) for pattern in patterns),
                filenames,
            )
            for filename in to_remove:
                os.remove(path + os.sep + filename)


    def check_dependencies_command(self, path):
        print("Rithm.check_dependencies_command")
        return
        path = Path(args.filename)
        g = create_graph(path)
        result, cycle = has_cycle(g)
        if result:
            print(f"Found cycle: {cycle}")
            sys.exit(1)
        print("Success!")


    def check_all_command(self, path):
        print("Rithm.check_all_command")
        return
        path = Path(args.path)
        cpp_extensions = ["cpp", "hpp", "h"]
        for ext in cpp_extensions:
            for file_path in path.glob(f"**/*.{ext}"):
                print(file_path)
                # continue
                g = create_graph(file_path)
                result, cycle = has_cycle(g)
                if result:
                    print(f"Found cycle: {cycle}")
                    sys.exit(1)

        check_pragma(path)
        print("Success!")





rithm = Rithm()