import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

from .links import *
from .problem_info import ProblemInfo
from .verdict import Verdict


class SeleniumCodeforces:
    _WAITING_TIME = 5

    def __init__(self, handle, password):
        self.handle = handle
        self.password = password
        self.browser = None

    def init(self):
        # TODO: there are some local issues in using Chrome instead of Firefox
        # self.browser = webdriver.Chrome()

        # snap installed firefox needs it
        text = subprocess.check_output("whereis geckodriver", shell=True, text=True)
        pattern = r"geckodriver: (?P<path>.*?)\s+"
        path = re.search(pattern, text).group("path")
        service = webdriver.FirefoxService(path)

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        self.browser = webdriver.Firefox(service=service, options=options)

    def close(self):
        self.browser.quit()

    def login(self):
        self.browser.get(login_link())
        time.sleep(self._WAITING_TIME)

        handle_element = self.browser.find_element(
            By.XPATH, "//input[@id='handleOrEmail']"
        )
        handle_element.clear()
        handle_element.send_keys(self.handle)

        password_element = self.browser.find_element(
            By.XPATH, "//input[@id='password']"
        )
        password_element.clear()
        password_element.send_keys(self.password)

        submit_element = self.browser.find_element(By.XPATH, "//input[@class='submit']")
        submit_element.click()

        time.sleep(self._WAITING_TIME)
        print(self.browser.current_url)
        # at least check something =(
        assert self.browser.current_url == f"{main_link()}/"
        print("Successfully logged in")

    def submit(self, submission_file: Path, problem_info: ProblemInfo):
        self.browser.get(submit_link(problem_info))
        time.sleep(self._WAITING_TIME)

        problem_option_element = self.browser.find_element(
            By.XPATH, f"//option[@value='{problem_info.problem}']"
        )
        problem_option_element.click()
        # TODO: choose language better
        language_option_element = self.browser.find_element(
            By.XPATH, "//option[@value='89']"
        )
        language_option_element.click()

        switch_off_editor_element = self.browser.find_element(
            By.XPATH, "//input[@id='toggleEditorCheckbox']"
        )
        if not switch_off_editor_element.is_selected():
            switch_off_editor_element.click()

        source_code_element = self.browser.find_element(By.ID, "sourceCodeTextarea")

        submission_text = submission_file.open().read()
        # make the submission unique
        guid = uuid.uuid4()
        print(f"Submission guid = {guid}")
        submission_text_unique = f"// {guid}\n {submission_text}"

        source_code_element.send_keys(submission_text_unique)

        submit_element = self.browser.find_element(
            By.XPATH, "//input[@id='singlePageSubmitButton']"
        )
        submit_element.click()

        time.sleep(self._WAITING_TIME)
        print(self.browser.current_url)
        assert self.browser.current_url == my_submissions_link(problem_info)
        print("Successfully submitted")

    def get_verdict(self, problem_info: ProblemInfo):
        self.browser.get(my_submissions_link(problem_info))

        for _ in range(5):
            time.sleep(self._WAITING_TIME)
            self.browser.refresh()

            submission_elements = self.browser.find_elements(
                By.CLASS_NAME, "highlighted-row"
            )
            submission_element = submission_elements[0]
            submission_id = submission_element.get_attribute("data-submission-id")

            status_element = submission_element.find_element(
                By.CLASS_NAME, "status-cell"
            )
            if status_element.get_attribute("waiting") == "false":
                verdict = status_element.text
                return Verdict.from_string(verdict)

        print("Can't get the problem's verdict for a long time")
        sys.exit(1)

    def get_source_code(self, submission_id):
        view_source_element = self.browser.find_element(
            By.XPATH, f"//*[@submissionid='{submission_id}' and @class='view-source']"
        )
        view_source_element.click()
        # TODO: get source code
        raise NotImplementedError(":(")
