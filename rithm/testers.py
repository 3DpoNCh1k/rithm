

from pathlib import Path
import sys
import tempfile

from .algo import Task
from .library_checker import LibraryChecker, ProblemChecker
from .compiler import *
from .codeforces import Codeforces, Verdict
from .algo import Algo

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
    
    def test(self, task: Task, testcase=None):
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

    def test(self, task: Task, testcase=None):
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
            self._produce_solution_outputs(solver_path, problem_checker, outputs_path, testcase)
            problem_checker.validate_testcases(outputs_path, testcase)

    def _produce_solution_outputs(self, solution_path, problem_checker: ProblemChecker, output_path, testcase=None):
        print("produce_solution_outputs")
        testcases = problem_checker.get_testcases()
        if testcase is not None:
            testcases = list(filter(lambda path: path.name == testcase, testcases))
        for testcase in testcases:
            name = testcase.name[:-3]
            my_output = output_path / f"{name}.out"
            self._produce_solution_output(solution_path, testcase, my_output)

    def _produce_solution_output(self, solution_path, testcase_path, output_path):
        self._run(solution_path, testcase_path, output_path)

    def _run(self, program, input_file, output_file):
        cmd = f"{program} < {input_file} > {output_file}"
        subprocess.check_call(cmd, shell=True)
    

class CodeforcesTester:
    def __init__(self, algo: Algo, codeforces: Codeforces):
        self.algo = algo
        self.codeforces = codeforces
    
    def test(self, task: Task, testcase=None):
        submission_text = self.algo.create_submission_text(task.solution_path)
        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            submission_path = build_path / "submission.cpp"
            submission_path.open("w").write(submission_text)
            result = self.codeforces.test_solution(task['link'], submission_path)
            print(result)
            if result != Verdict.AC:
                print("Failed")
                sys.exit(1)
            print("Accepted!")