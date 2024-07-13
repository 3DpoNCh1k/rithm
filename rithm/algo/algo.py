import sys
from pathlib import Path

from rithm.files.file import File
from rithm.utils.files import get_files_from_directory

from .cpp_file import AlgoCppFile
from .preprocessor import Preprocessor


class Algo:
    def __init__(self, path: Path):
        self.path = path
        self.preprocessor = Preprocessor()

    @property
    def source_code_path(self):
        return self.path / "algo"

    @property
    def tests_path(self):
        return self.path / "tests"

    def create_submission_text(self, file: Path):
        file = AlgoCppFile(file)
        text = self.preprocessor.expand_includes(file)
        return text

    def check_include_all(self):
        include_all_file = self.tests_path / "include_all.cpp"
        include_all_filenames = set(AlgoCppFile(include_all_file).algo_dependencies)
        algo_filenames = set(
            map(
                self.get_algo_name,
                get_files_from_directory(self.source_code_path, recursive=True),
            )
        )

        if algo_filenames != include_all_filenames:
            not_included = algo_filenames - include_all_filenames
            not_exist = include_all_filenames - algo_filenames
            if not_included:
                print(f"Files that are not included: {sorted(not_included)}")
            if not_exist:
                print(f"Files that does not exist: {sorted(not_exist)}")

    def generate_include_all(self, filenames):
        return "\n".join(f"#include <{name}>" for name in sorted(filenames))

    def check_extensions(self):
        consistent_extension = "hpp"
        for file in get_files_from_directory(self.source_code_path, recursive=True):
            if File(file).extension != consistent_extension:
                print(f'{file} is not a "{consistent_extension}" file')
                sys.exit(1)

    def get_algo_name(self, file: Path):
        return str(file.relative_to(self.path))
