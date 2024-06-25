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
from .testers import *


class Rithm:
    def __init__(self):
        self.algo_path = ALGO_PATH
        self.algo = Algo(self.algo_path)
        self.library_checker = LibraryChecker(LIBRARY_CHECKER_DIRECTORY)
        self.config = load_config()

    def build_command(self, profile, input_file, output_file):
        assert input_file[-4:] == ".cpp"
        profile = self.config[profile]
        options = Options(compiler=profile["compiler"], others=profile["options"])
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
        if task.has_library_checker_tests() and task.has_library_checker_solution():
            tester = LibraryCheckerTester(self.algo_path, self.library_checker)
            tester.test(task)
        
        if task.has_local_tests():
            tester = Tester(self.algo_path)
            tester.test(task)


rithm = Rithm()
