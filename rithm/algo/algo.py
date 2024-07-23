import re
import sys
import tempfile
from pathlib import Path

from rithm.files.file import File
from rithm.staff.compiler import create_default_compiler
from rithm.utils.files import get_files_from_directory

from .cpp_file import AlgoCppFile
from .preprocessor import Preprocessor


class Algo:
    def __init__(self, path: Path):
        self.path = path
        self.preprocessor = Preprocessor(self.path)

    @property
    def source_code_path(self):
        return self.path / "algo"

    @property
    def tests_path(self):
        return self.path / "tests"

    def create_submission_text(self, file: Path):
        file = AlgoCppFile(file)
        text = self.preprocessor.expand_includes(file)
        self._validate(text)
        return text

    def check_extensions(self):
        consistent_extension = ".hpp"
        for file in get_files_from_directory(self.source_code_path, recursive=True):
            if File(file).extension != consistent_extension:
                print(f'{file} is not a "{consistent_extension}" file')
                sys.exit(1)

    def check_bad_patterns(self):
        bad_source_code_includes = ["algo/utils/debug.hpp", "iostream"]
        bad_source_code_patterns = [
            (r"using\s+namespace\s+std\s*;", "Don't expose whole std namespace"),
            (r"std::cout", "Dont'use stdout stream"),
            (r"std::cin", "Dont'use stdin stream"),
        ]
        bad_patterns = [
            (r"dbg\(", "Remove debugging code"),
            (r"#include\s+\"", "Don't use quoted includes"),
        ]
        found_errors = False
        for file in get_files_from_directory(self.source_code_path, recursive=True):
            file = AlgoCppFile(file)
            for algo_dependency in file.algo_dependencies:
                if algo_dependency in bad_source_code_includes:
                    print(
                        f"File {file.path} has {algo_dependency} as an include dependency"
                    )
                    found_errors = True
            if file.tests_dependencies:
                print(
                    f"File {file.path} has {file.tests_dependencies} as include dependencies"
                )
                found_errors = True

            if self._get_algo_name(file.path) == "algo/utils/debug.hpp":
                continue

            for pattern, hint in bad_patterns + bad_source_code_patterns:
                m = re.search(pattern, file.text)
                if m:
                    s = file.text[m.start() : m.end()]
                    print(
                        f"File {file.path} has a bad pattern: substring '{s}' matches '{pattern}' pattern.\nHint: {hint}"
                    )
                    found_errors = True
        if found_errors:
            sys.exit(1)

    def check_dependency_cycle(self, file: Path):
        file = AlgoCppFile(file)
        self.preprocessor.check_dependency_cycle(file)

    def format_includes(self, file: Path):
        algo_file = AlgoCppFile(file)
        text = algo_file.text
        found = False
        for dependency in algo_file.algo_dependencies + algo_file.tests_dependencies:
            m = re.search(rf'#include\s+"{dependency}"', text)
            if m:
                found = True
                before = text[: m.start()]
                after = text[m.end() :]
                text = before + f"#include <{dependency}>" + after

        if found:
            algo_file.path.open("w").write(text)

    def _get_algo_name(self, file: Path):
        return str(file.relative_to(self.path))

    def _validate(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            compiler = create_default_compiler(self.path)
            input_file = Path(directory) / "input.cpp"
            input_file.open("w").write(text)
            output_file = Path(directory) / "output"
            compiler.compile_file(input_file, output_file)
