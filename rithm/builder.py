from pathlib import Path

from rithm.compiler import create_compiler
from rithm.source_files import CppFile


class Builder:
    def __init__(self, config):
        self.config = config

    def build(self, profile, input_file, output_file=None):
        input_file = CppFile(input_file)
        output_path = (
            Path(output_file)
            if output_file is not None
            else self.get_default_output_path(input_file)
        )
        profile = self.config[profile]
        compiler = create_compiler(self.algo_path, self.config[profile])
        compiler.compile_file(input_file.path, output_path)

    def get_default_output_path(input_file: CppFile):
        current_directory = Path(".").absolute()
        suffix = input_file.directory.relative_to(current_directory)
        output_path = (
            current_directory
            / "build"
            / suffix
            / input_file.name_without_extension
            / ".out"
        )
        return output_path
