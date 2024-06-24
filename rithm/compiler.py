from dataclasses import dataclass
from pathlib import Path
import subprocess

from .config import ALGO_PATH


def compile_solver(solution_path, solver_path):
    cmd = f"g++ --std=c++17 -I {ALGO_PATH} -Wall -Wextra -Wshadow -fsanitize=address -fsanitize=undefined -o {solver_path} {solution_path}"
    subprocess.check_call(cmd, shell=True)

@dataclass
class Options:
    compiler: str
    std: int
    includes: list[Path]
    sanitizers: list[str]
    warnings: list[str]

class Compiler:
    def __init__(self, options: Options):
        self.options = options

    def compile_file(self, input_file, output_file):
        cmd = f"{self.compilation_line} -o {output_file} {input_file}"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    @property
    def compilation_line(self):
        includes_line = " ".join(f"-I {path}" for path in self.options.includes)
        warnings_line = " ".join(f"-W{warning}" for warning in self.options.warnings)
        sanitizers_line = " ".join(f"-fsanitize={sanitizer}" for sanitizer in self.options.sanitizers)
        with_extra_spaces = f"{self.options.compiler} --std=c++{self.options.std} {includes_line} {warnings_line} {sanitizers_line}"
        without_extra_spaces = " ".join(with_extra_spaces.split())
        return without_extra_spaces
