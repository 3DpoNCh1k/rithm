import sys
import tempfile
from pathlib import Path

from rithm.algo import Algo
from rithm.codeforces import Codeforces, Verdict
from rithm.tasks.codeforces import CodeforcesTask


class CodeforcesTester:
    def __init__(self, algo: Algo, codeforces: Codeforces):
        self.algo = algo
        self.codeforces = codeforces

    def test(self, task: CodeforcesTask, testcase=None):
        submission_text = self.algo.create_submission_text(task.solution)
        with tempfile.TemporaryDirectory() as temporary_build_directory:
            build_path = Path(temporary_build_directory)
            submission_path = build_path / "submission.cpp"
            submission_path.open("w").write(submission_text)
            result = self.codeforces.test_solution(task.link, submission_path)
            print(result)
            if result != Verdict.AC:
                print("Failed")
                sys.exit(1)
            print("Accepted!")
