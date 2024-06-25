

from pathlib import Path
import tempfile

from .algo import Task
from .library_checker import LibraryChecker, ProblemChecker
from .compiler import *

def create_default_compiler(algo_path):
    options = Options(
        compiler="g++",
        std=17,
        includes=[algo_path],
        sanitizers=["address", "undefined"],
        warnings=["all", "extra", "shadow"],
        others="-O2"
    )
    return Compiler(options)

class Tester:
    def __init__(self, algo_path):
        self.algo_path = algo_path
    
    def test(self, task: Task):
        compiler = create_default_compiler(self.algo_path)
        
        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            test_runner_path = build_path / "test_runner"
            compiler.compile_file(task.target_path, test_runner_path)
            cmd = f"{test_runner_path}"
            print(cmd)
            subprocess.check_call(cmd, shell=True)
            print("Success!")
            

class LibraryCheckerTester:
    def __init__(self, algo_path, library_checker: LibraryChecker):
        self.algo_path = algo_path
        self.library_checker = library_checker

    def test(self, task: Task):
        problem_checker = self.library_checker.create_problem_checker(
            Path(task["library-checker-problems"])
        )
        problem_checker.generate_testcases()

        compiler = create_default_compiler(self.algo_path)
        
        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            outputs_path = build_path / "outputs"
            outputs_path.mkdir(exist_ok=True)
            solver_path = build_path / "solver"
            compiler.compile_file(task.solution_path, solver_path)
            self._produce_solution_outputs(solver_path, problem_checker, outputs_path)
            problem_checker.validate_testcases(outputs_path)

    def _produce_solution_outputs(self, solution_path, problem_checker: ProblemChecker, output_path):
        print("produce_solution_outputs")
        for testcase in problem_checker.get_testcases():
            name = testcase.name[:-3]
            my_output = output_path / f"{name}.out"
            self._produce_solution_output(solution_path, testcase, my_output)

    def _produce_solution_output(self, solution_path, testcase_path, output_path):
        self._run(solution_path, testcase_path, output_path)

    def _run(self, program, input_file, output_file):
        cmd = f"{program} < {input_file} > {output_file}"
        subprocess.check_call(cmd, shell=True)