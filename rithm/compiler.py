import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Options:
    compiler: str
    std: int = None
    includes: list[Path] = field(default_factory=list)
    optimization: str = "0"
    sanitizers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    others: str = ""


class Compiler:
    def __init__(self, options: Options):
        # TODO: support clang
        assert options.compiler == "g++"
        self.options = options

    def compile_file(self, input_file, output_file):
        cmd = f"{self.compilation_line} -o {output_file} {input_file}"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    @property
    def compilation_line(self):
        includes_line = " ".join(f"-I {path}" for path in self.options.includes)
        warnings_line = " ".join(f"-W{warning}" for warning in self.options.warnings)
        optimization_line = f"-O{self.options.optimization}"
        sanitizers_line = " ".join(
            f"-fsanitize={sanitizer}" for sanitizer in self.options.sanitizers
        )
        standard_line = f"--std=c++{self.options.std}" if self.options.std else ""
        with_extra_spaces = f"{self.options.compiler} {standard_line} {includes_line} {warnings_line} {optimization_line} {sanitizers_line} {self.options.others}"
        without_extra_spaces = " ".join(with_extra_spaces.split())
        return without_extra_spaces


def create_default_compiler(algo_path):
    options = Options(
        compiler="g++",
        std=17,
        includes=[algo_path],
        optimization="2",
        sanitizers=["address", "undefined"],
        warnings=["all", "extra", "shadow"],
    )
    return Compiler(options)


def create_compiler(algo_path, profile):
    options = Options(**profile)
    options.includes += [algo_path]
    return Compiler(options)
