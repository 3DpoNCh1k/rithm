import sys
import time
from pathlib import Path

import requests
from robobrowser import RoboBrowser

from .links import *
from .problem_info import ProblemInfo
from .verdict import Verdict


class RobobrowserCodeforces:
    def __init__(self, handle, password):
        self.handle = handle
        self.password = password
        self.browser = RoboBrowser()

    def login(self):
        self.browser.open(login_link())
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

    def submit(self, submission_file: Path, problem_info: ProblemInfo):
        submission_text = submission_file.open().read()
        self.browser.open(submit_link(problem_info))

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
            self.browser.open(my_submissions_link(problem_info))

            submissions_table = self.browser.find(
                lambda tag: tag.name == "table"
                and tag.has_attr("class")
                and "status-frame-datatable" in tag["class"]
            )

            submissions = submissions_table.find_all("tr")

            # submissions[0] - header
            submission = submissions[1]
            assert submission.has_attr("data-submission-id")
            submission_id = submission["data-submission-id"]

            # find columns
            submission_columns = submission.find_all("td")
            verdict = submission_columns[5]
            if verdict["waiting"] == "true":
                continue

            assert verdict["waiting"] == "false"
            verdict_span = verdict.find_all("span")[1]
            return Verdict.from_string(verdict_span.text)

        print("Can't get the problem's verdict for a long time")
        sys.exit(1)

    def get_source_code(self, submission_id, problem_info: ProblemInfo):
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
        response = requests.post(
            get_source_code_link(problem_info), data=payload, header=header
        )
        return response.json()["source"]
