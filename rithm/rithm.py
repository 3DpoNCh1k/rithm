import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .algo import *
from .codeforces import *
from .compiler import *
from .config import *
from .contest import *
from .graph import *
from .library_checker import *
from .secrets import *
from .stress import *
from .tasks import *
from .testers import *
from .utils import *


class Rithm:
    def __init__(self):
        self.algo_path = ALGO_PATH
        self.algo = Algo(self.algo_path)
        self.library_checker = LibraryChecker(LIBRARY_CHECKER_DIRECTORY)
        self.config = load_config()
        self.secrets = load_secrets()
        self.codeforces = Codeforces(
            self.secrets["codeforces"]["handle"], self.secrets["codeforces"]["password"]
        )
        self.contest = Contest()
        self.stress = Stress()

    def build_command(self, profile, input_file, output_file):
        assert input_file[-4:] == ".cpp"
        profile = self.config[profile]
        compiler = create_compiler(self.algo_path, self.config[profile])
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

    def run_command(self, profile, filename, input_file):
        assert filename[-4:] == ".cpp"

        compiler = create_compiler(self.algo_path, self.config[profile])
        print(compiler.compilation_line)

        with tempfile.TemporaryDirectory() as temporary_run_directory:
            run_path = Path(temporary_run_directory)
            solver_path = run_path / "solver"
            compiler.compile_file(filename, solver_path)
            cmd = f"{solver_path}" + ("" if input_file is None else f" < {input_file}")
            subprocess.check_call(cmd, shell=True)

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

    def test_command(self, path, type):
        path = Path(path)

        target_class = None
        if type == "local":
            target_class = TestTask
        if type == "library-checker":
            target_class = LibraryCheckerTask
        if type == "codeforces":
            target_class = CodeforcesTask

        tasks = self.algo.get_all_tasks(path, target_class)
        for task in tasks:
            self._process_task(task)

    def test_task_command(self, path, testcase):
        path = Path(path)
        print(testcase)
        for task in self.algo.get_tasks(path):
            self._process_task(task, testcase)

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

        self.algo.check_extensions()
        self.algo.check_include_all()
        print("Success!")

    def stress_create_command(self):
        self.stress.create()

    def stress_run_command(self):
        self.stress.run()

    def contest_create_command(self, problems):
        self.contest.create_problems(problems)

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

    def _process_task(self, task, testcase=None):
        if isinstance(task, LibraryCheckerTask):
            tester = LibraryCheckerTester(self.algo_path, self.library_checker)
            tester.test(task, testcase)

        if isinstance(task, TestTask):
            tester = Tester(self.algo_path, self.config)
            tester.test(task, testcase)

        if isinstance(task, CodeforcesTask):
            tester = CodeforcesTester(self.algo, self.codeforces)
            tester.test(task, testcase)


rithm = Rithm()
