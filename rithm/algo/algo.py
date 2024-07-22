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
        bad_source_code_includes = ["algo/utils/debug.hpp"]
        bad_patterns = [r"dbg\("]
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

            for pattern in bad_patterns:
                m = re.search(pattern, file.text)
                if m:
                    s = file.text[m.start() : m.end()]
                    print(
                        f"File {file.path} has a bad pattern: substring '{s}' matches '{pattern}' pattern"
                    )
                    found_errors = True
        if found_errors:
            sys.exit(1)

    def check_dependency_cycle(self, file: Path):
        file = AlgoCppFile(file)
        self.preprocessor.check_dependency_cycle(file)

    def _get_algo_name(self, file: Path):
        return str(file.relative_to(self.path))

    def _validate(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            compiler = create_default_compiler(self.path)
            input_file = Path(directory) / "input.cpp"
            input_file.open("w").write(text)
            output_file = Path(directory) / "output"
            compiler.compile_file(input_file, output_file)
