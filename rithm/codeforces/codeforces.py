import re
import sys

from .problem_info import ProblemInfo
from .robobrowser_cf import RobobrowserCodeforces
from .selenium_cf import SeleniumCodeforces


class Codeforces:
    def __init__(self, handle, password):
        self.impl = SeleniumCodeforces(handle, password)

    def test_solution(self, problem_link, solution_path):
        try:
            pattern = r"https://codeforces.com/group/(?P<group>.*)/contest/(?P<contest>.*)/problem/(?P<problem>.*)"
            group, contest, problem = re.search(pattern, problem_link).groups()
            problem_info = ProblemInfo(group, contest, problem)
        except:
            print(f"Currently only the following format is supported: {pattern}")
            sys.exit(1)

        print(problem_info)
        try:
            self.impl.init()
            self.impl.login()
            self.impl.submit(solution_path, problem_info)
            verdict = self.impl.get_verdict(problem_info)
        finally:
            self.impl.close()

        return verdict
