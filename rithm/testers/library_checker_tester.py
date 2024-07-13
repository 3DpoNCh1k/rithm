import subprocess
import tempfile
from pathlib import Path

from rithm.compiler import create_default_compiler
from rithm.library_checker import LibraryChecker, ProblemChecker
from rithm.task import LibraryCheckerTask


class LibraryCheckerTester:
    def __init__(self, algo_path, library_checker: LibraryChecker):
        self.algo_path = algo_path
        self.library_checker = library_checker

    def test(self, task: LibraryCheckerTask, testcase=None):
        problem_checker = self.library_checker.create_problem_checker(task.problem)
        problem_checker.generate_testcases()

        compiler = create_default_compiler(self.algo_path)

        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            outputs_path = build_path / "outputs"
            outputs_path.mkdir(exist_ok=True)
            solver_path = build_path / "solver"
            compiler.compile_file(task.solution, solver_path)
            self._produce_solution_outputs(
                solver_path, problem_checker, outputs_path, testcase
            )
            problem_checker.validate_testcases(outputs_path, testcase)

    def _produce_solution_outputs(
        self,
        solution: Path,
        problem_checker: ProblemChecker,
        output_path,
        testcase=None,
    ):
        print("produce_solution_outputs")
        testcases = problem_checker.get_testcases()
        if testcase is not None:
            testcases = list(filter(lambda path: path.name == testcase, testcases))
        for testcase in testcases:
            name = testcase.name[:-3]
            my_output = output_path / f"{name}.out"
            self._produce_solution_output(solution, testcase, my_output)

    def _produce_solution_output(self, solution: Path, testcase_path, output_path):
        self._run(solution, testcase_path, output_path)

    def _run(self, program, input_file, output_file):
        cmd = f"{program} < {input_file} > {output_file}"
        subprocess.check_call(cmd, shell=True)
