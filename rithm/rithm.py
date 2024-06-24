import os
import subprocess
from pathlib import Path
import re
import sys
import tempfile


from .config import *
from .graph import *
from .utils import *
from .library_checker import *
from .algo import *
from .compiler import *


class Rithm:
    def __init__(self):
        self.algo = Algo(ALGO_PATH)
        self.library_checker = LibraryChecker(LIBRARY_CHECKER_DIRECTORY)
        self.config = load_config()
    

    def build_command(self, profile, input_file, output_file):
        assert input_file[-4:] == ".cpp"
        profile = self.config[profile]
        options = Options(
            compiler=profile["compiler"],
            others=profile["options"]
        )
        compiler = Compiler(options)
        print(compiler.compilation_line)
        print(input_file)
        print(output_file)
        input_path = Path(input_file)
        assert not input_path.is_absolute()
        if output_file is None:
            name = os.path.splitext(input_path.name)[0]
            folder = input_path.parent
            build_folder = Path("build") / folder
            build_folder.mkdir(parents=True, exist_ok=True)
            output_file = build_folder / f"{name}.exe"
        
        print(output_file)
        compiler.compile_file(input_file, output_file)


    def run_command(self, profile, compiler, filename, local_debug):
        local_debug = bool(local_debug)
        assert filename[-4:] == ".cpp"
        executable = filename[:-4] + ".exe"

        config = self.config["compiler"][compiler]
        std = config["std"]
        always_flags = config["always"]
        profile_flags = config["profiles"][profile]
        debug_flags = config["localDebug"] if local_debug else ""

        cmd_line = f"--std={std} {always_flags} {profile_flags} {debug_flags}"

        options = Options(compiler=compiler, others=cmd_line)

        compiler = Compiler(options)
        print(compiler.compilation_line)

        if os.path.exists(executable):
            os.remove(executable)

        compiler.compile_file(filename, executable)
        res = subprocess.run(executable, shell=True, check=True)
        assert res.returncode == 0
        print("Success!")

    def prepare_submission_command(self, filename):
        file_path = Path(filename)
        submission_text = self.algo.create_submission_text(file_path)
        name = file_path.name
        print(os.getcwd())
        folder = file_path.parent
        new_folder_path = Path(".") / "submit" / folder.name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        open(new_folder_path / f"submission_{name}", "w").write(submission_text)

    def test_command(self, path):
        path = Path(path)
        tasks = self.algo.get_all_tasks(path)
        for task in tasks:
            self._process_task(task)

    def clean_command(self, path):
        path = Path(path).absolute()
        patterns = [".*\.exe$", ".*\.exp$", ".*\.lib$", ".*\.pdb$"]
        for pathname, _, filenames in os.walk(path):
            to_remove = filter(
                lambda filename: any(
                    re.match(pattern, filename) for pattern in patterns
                ),
                filenames,
            )
            for filename in to_remove:
                os.remove(Path(pathname) / filename)

    def check_dependencies_command(self, filename):
        self._check_dependency_cycle(Path(filename))
        print("Success!")

    def check_all_command(self, path):
        path = Path(path)
        cpp_extensions = ["cpp", "hpp", "h"]
        for ext in cpp_extensions:
            for file_path in path.glob(f"**/*.{ext}"):
                print(file_path)
                self._check_dependency_cycle(file_path)

        self._check_pragma(path)
        print("Success!")

    def _check_dependency_cycle(self, file_path):
        g = create_graph(file_path)
        result, cycle = has_cycle(g)
        if result:
            print(f"Found cycle: {cycle}")
            sys.exit(1)

    def _check_pragma(self, path):
        header_extensions = ["hpp", "h"]
        for ext in header_extensions:
            for file_path in path.glob(f"**/*.{ext}"):
                if not has_pragma(file_path):
                    print(f"File {file_path} does not has #pragma once")
                    sys.exit(1)

        print("Success!")

    def _process_task(self, task: Task):
        if task.has_local_tests() and task.has_solution():
            self._test_task(task)

    def _test_task(self, task: Task):
        problem_checker = self.library_checker.create_problem_checker(
            Path(task["library-checker-problems"])
        )
        problem_checker.generate_testcases()

        options = Options(
            compiler="g++",
            std=17,
            includes=[ALGO_PATH],
            sanitizers=["address", "undefined"],
            warnings=["all", "extra", "shadow"],
        )
        compiler = Compiler(options)

        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            outputs_path = build_path / "outputs"
            outputs_path.mkdir(exist_ok=True)
            solver_path = build_path / "solver"
            compiler.compile_file(task.solution_path, solver_path)
            self._produce_solution_outputs(solver_path, problem_checker, outputs_path)
            problem_checker.validate_testcases(outputs_path)

    def _produce_solution_outputs(self, solution_path, problem_checker, output_path):
        print("produce_solution_outputs")
        for testcase in problem_checker.get_testcases():
            name = testcase.name[:-3]
            my_output = output_path / f"{name}.out"
            self._produce_solution_output(solution_path, testcase, my_output)

    def _produce_solution_output(self, solution_path, testcase_path, output_path):
        self._run(solution_path, testcase_path, output_path)

    def _run(self, program, input_file, output_file):
        cmd = f"{program} < {input_file} > {output_file}"
        subprocess.check_call(cmd, shell=True)


rithm = Rithm()
