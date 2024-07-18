import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Options:
    compiler: str
    std: int
    includes: list[Path] = field(default_factory=list)
    optimization: str = "0"
    sanitizers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    others: str = ""


class CompilationError(RuntimeError):
    def __init__(self, cmd, output):
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return "\n".join(
            [
                "Compilation error",
                "Failed command:",
                f"{self.cmd}",
                "Output:",
                f"{self.output}",
            ]
        )


class Compiler:
    def __init__(self, options: Options):
        # TODO: support clang
        assert options.compiler == "g++"
        self.options = options

    def compile_file(self, input_file, output_file):
        cmd = f"{self.compilation_line} -o {output_file} {input_file}"
        proc = subprocess.run(
            cmd,
            check=False,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.returncode != 0:
            text = proc.stdout
            match = re.search("error", text)
            assert match
            matched_text = text[match.start() : match.end()]
            text_before = text[: match.start()]
            text_after = text[match.end() :]
            lines_before = text_before.split("\n")
            lines_after = text_after.split("\n")
            LINES_BEFORE = 1
            LINES_AFTER = 15
            output = (
                "\n".join(lines_before[-LINES_BEFORE:])
                + matched_text
                + "\n".join(lines_after[:LINES_AFTER])
            )
            raise CompilationError(cmd, output)

    @property
    def compilation_line(self):
        compiler = f"{self.options.compiler}"
        standard = f"--std=c++{self.options.std}"
        includes = " ".join(f"-I {path}" for path in self.options.includes)
        warnings = " ".join(f"-W{warning}" for warning in self.options.warnings)
        optimization = f"-O{self.options.optimization}"
        sanitizers = " ".join(
            f"-fsanitize={sanitizer}" for sanitizer in self.options.sanitizers
        )
        others = self.options.others

        with_extra_spaces = f"{compiler} {standard} {includes} {warnings} {optimization} {sanitizers} {others}"
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
