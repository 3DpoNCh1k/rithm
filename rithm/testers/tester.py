import subprocess
import tempfile
from pathlib import Path

from rithm.compiler import create_compiler
from rithm.task import TestTask


class Tester:
    def __init__(self, algo_path, config):
        self.algo_path = algo_path
        self.config = config

    def test(self, task: TestTask, testcase=None):
        compiler = create_compiler(self.algo_path, self.config[task.profile])

        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            test_runner_path = build_path / "test_runner"
            compiler.compile_file(task.target, test_runner_path)
            cmd = f"{test_runner_path}"
            print(cmd)
            subprocess.check_call(cmd, shell=True)
            print("Success!")
