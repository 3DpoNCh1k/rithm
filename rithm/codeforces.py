from dataclasses import dataclass
from enum import Enum
import re
import sys
import time
import requests
from robobrowser import RoboBrowser


@dataclass
class ProblemInfo:
    group: str
    contest: str
    problem: str


class Verdict(Enum):
    AC = 1
    WA = 2
    RE = 3
    MLE = 4
    TLE = 5
    CE = 6

    @staticmethod
    def from_string(s: str):
        s = s.lower()
        if s == "accepted":
            return Verdict.AC
        if s == "wrong answer":
            return Verdict.WA
        if s == "runtime error":
            return Verdict.RE
        if s == "memory limit exceeded":
            return Verdict.MLE
        if s == "time limit exceeded":
            return Verdict.TLE
        if s == "compilation error":
            return Verdict.CE

        raise ValueError(f"Unknown verdict {s}")


class Codeforces:
    def __init__(self, handle, password):
        self.handle = handle
        self.password = password
        self.browser = RoboBrowser()

    def test_solution(self, problem_link, solution_path):
        try:
            pattern = r"https://codeforces.com/group/(?P<group>.*)/contest/(?P<contest>.*)/problem/(?P<problem>.*)"
            group, contest, problem = re.search(pattern, problem_link).groups()
            problem_info = ProblemInfo(group, contest, problem)
        except:
            print(f"Currenlt only the following format is supported: {pattern}")
            sys.exit(1)

        print(problem_info)
        # self.login()
        # self.submit(solution_path, problem_info)
        # return self.get_verdict(problem_info)

    def login(self):
        self.browser.open("https://codeforces.com/enter")
        enter_form = self.browser.get_form("enterForm")
        enter_form["handleOrEmail"] = self.handle
        enter_form["password"] = self.password

        self.browser.submit_form(enter_form)

        checks = list(
            map(
                lambda x: x.getText()[1:].strip(),
                self.browser.select("div.caption.titled"),
            )
        )
        assert self.handle in checks

    def submit(self, submission_file, problem_info: ProblemInfo):
        submission_text = submission_file.open().read()
        submit_link = f"https://codeforces.com/group/{problem_info.group}/contest/{problem_info.contest}/submit"
        self.browser.open(submit_link)

        submit_form = self.browser.get_form(class_="submit-form")
        submit_form["submittedProblemIndex"] = problem_info.problem
        # 89 is C++20 (GCC 13-64)
        submit_form["programTypeId"] = 89
        submit_form["source"] = submission_text

        self.browser.submit_form(submit_form)
        # add asserts that everything is ok

    def get_verdict(self, problem_info: ProblemInfo):
        for _ in range(5):
            time.sleep(5)
            my_submissions_link = f"https://codeforces.com/group/{problem_info.group}/contest/{problem_info.contest}/my"
            self.browser.open(my_submissions_link)

            # find submission table
            table = self.browser.find(
                lambda tag: tag.name == "table"
                and tag.has_attr("class")
                and "status-frame-datatable" in tag["class"]
            )

            # find rows
            rows = table.find_all("tr")

            # rows[0] - header
            # assume that rows[1] is our submission
            submission_row = rows[1]
            assert submission_row.has_attr("data-submission-id")
            submission_id = submission_row["data-submission-id"]

            # find columns
            submission_columns = submission_row.find_all("td")
            verdict = submission_columns[5]
            if verdict["waiting"] == "true":
                continue

            assert verdict["waiting"] == "false"
            verdict_span = verdict.find_all("span")[1]
            return Verdict.from_string(verdict_span.text)

        print("Can't get the problem's verdict for a long time")
        sys.exit(1)

    def get_source_code(self, submission_id, problem_info: ProblemInfo):
        link = f"https://codeforces.com/group/{problem_info.group}/data/submitSource"
        payload = {
            "submissionId": submission_id,
        }
        csrf_token = ""
        session_id = ""
        header = {
            "Host": "codeforces.com",
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Csrf-Token": csrf_token,
            "Origin": "https://codeforces.com",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={session_id}",
        }
        response = requests.post(link, data=payload, header=header)
        return response.json()["source"]
