from pathlib import Path

from rithm.files.cpp import CppFile

from .compiler import create_compiler


class Builder:
    def __init__(self, config, algo_path):
        self.config = config
        self.algo_path = algo_path

    def build(self, profile, input_file, output_file=None):
        input_file = CppFile(input_file)
        output_path = (
            Path(output_file)
            if output_file is not None
            else self.get_default_output_path(input_file)
        )
        compiler = create_compiler(self.algo_path, self.config[profile])
        compiler.compile_file(input_file.path, output_path)

    def get_default_output_path(self, input_file: CppFile):
        current_directory = Path(".").absolute()
        suffix = input_file.directory.relative_to(current_directory)
        output_directory = current_directory / "build" / suffix
        output_directory.mkdir(parents=True, exist_ok=True)
        output_path = output_directory / f"{input_file.name_without_extension}.out"
        return output_path
