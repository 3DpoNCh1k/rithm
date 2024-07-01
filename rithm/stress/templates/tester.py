import json
import os
import subprocess
import sys
import time
from pathlib import Path

STRESS_DIRECTORY = Path(os.path.realpath(__file__)).parent


class Tester:
    TIME_INTERVAL_BETWEEN_REPORTS = 10
    MAX_LEN = 50
    SEPARATOR_LINE = "~" * MAX_LEN

    def __init__(self):
        task_path = STRESS_DIRECTORY / "task.json"
        self.task = json.load(task_path.open())
        self.generated_path = STRESS_DIRECTORY / "generated"
        self.generated_path.mkdir(exist_ok=True)
        assert self.run_generator_command != ""
        assert self.run_correct_solver_command != ""
        assert self.run_solver_command != ""

    def test(self):
        testcase = 0
        print("Testing")
        last_report_time = time.time()
        while True:
            testcase += 1
            generated_input_path = self.generated_path / "input.txt"
            self._run(f"{self.run_generator_command} > {generated_input_path}")
            correct_output = self._run(
                f"{self.run_correct_solver_command} < {generated_input_path}"
            )
            output = self._run(f"{self.run_solver_command} < {generated_input_path}")
            if output != correct_output:
                correct_output_path = self.generated_path / "correct_output.txt"
                correct_output_path.open("w").write(correct_output)
                output_path = self.generated_path / "output.txt"
                output_path.open("w").write(output)
                text = "\n".join(
                    [
                        self.SEPARATOR_LINE,
                        "output != correct_output",
                        self.SEPARATOR_LINE,
                        "Output:",
                        self._cut(output),
                        self.SEPARATOR_LINE,
                        "Correct output:",
                        self._cut(correct_output),
                        self.SEPARATOR_LINE,
                    ]
                )
                print(text)
                sys.exit(1)

            if time.time() - last_report_time > self.TIME_INTERVAL_BETWEEN_REPORTS:
                print(f"{testcase} testcases passed")
                last_report_time = time.time()

    def _run(self, cmd):
        return subprocess.check_output(cmd, shell=True, text=True)

    def _cut(self, text):
        if len(text) > self.MAX_LEN:
            text = text[: self.MAX_LEN - 3] + "..."
        return text

    @property
    def run_generator_command(self):
        return self.task["run_generator_command"]

    @property
    def run_correct_solver_command(self):
        return self.task["run_correct_solver_command"]

    @property
    def run_solver_command(self):
        return self.task["run_solver_command"]


def main():
    tester = Tester()
    tester.test()


if __name__ == "__main__":
    main()
