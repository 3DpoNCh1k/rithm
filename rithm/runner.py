import subprocess


class Runner:
    def __init__(self):
        pass

    def _run(self, program, input_file=None, output_file=None, capture_output=False):
        return subprocess.check_call(
            program,
            stdin=input_file,
            stdout=output_file,
            stderr=output_file,
            capture_output=capture_output,
        )

    def run(self, program, input_file=None, output_file=None):
        self._run(program, input_file, output_file)

    def run_capture_output(self, program, input_file=None):
        return self._run(program, input_file, capture_output=True).stdout.decode()
