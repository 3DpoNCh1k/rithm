import os
import subprocess
from pathlib import Path
import re
import sys


from .config import *
from .graph import *
from .utils import *
from .library_checker import *
from .algo import *
from .compiler import *


def process_task(task: Task):
    if task.has_local_tests() and task.has_solution():
        test_task(task)


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
        local_debug = bool(local_debug)
        print("Rithm.run_command")
        return

        assert filename[-4:] == ".cpp"
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
                lambda filename: any(
                    re.match(pattern, filename) for pattern in patterns
                ),
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
