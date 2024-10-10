import subprocess


class Runner:
    def __init__(self):
        pass

    def _run(self, program, input_file=None, stdout_file=None, stderr_file=None):
        print("Runner._run", program, input_file, stdout_file, stderr_file)
        return subprocess.run(
            program,
            stdin=input_file,
            stdout=stdout_file,
            stderr=stderr_file,
            check=True,
        )

    def run(self, program, input_file=None, output_file=None):
        self._run(program, input_file, output_file, output_file)

    def run_capture_output(self, program, input_file=None):
        return self._run(
            program, input_file, subprocess.PIPE, subprocess.STDOUT
        ).stdout.decode()
