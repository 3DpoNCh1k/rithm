import sys
from pathlib import Path

from rithm.utils.files import get_files_from_directory

from .runner import Runner


class ExamplesRunner:
    MAX_LEN = 50
    SEPARATOR_LINE = "~" * MAX_LEN

    def run(self, program, examples):
        examples = Path(examples)
        assert examples.is_dir()
        runner = Runner()
        for example_input_file in sorted(get_files_from_directory(examples / "in")):
            print(f"Running {example_input_file.name}")
            example_output_file = examples / "out" / example_input_file.name
            assert example_output_file.exists()
            correct_output = example_output_file.open().read()
            output = runner.run_capture_output(program, example_input_file.open())
            if correct_output != output:
                text = "\n".join(
                    [
                        self.SEPARATOR_LINE,
                        "output != correct_output",
                        self.SEPARATOR_LINE,
                        "output:",
                        output,
                        self.SEPARATOR_LINE,
                        "correct_output:",
                        correct_output,
                        self.SEPARATOR_LINE,
                    ]
                )
                print(text)
                sys.exit(1)
