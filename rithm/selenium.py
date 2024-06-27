from pathlib import Path
import re
import subprocess
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .codeforces import ProblemInfo


def draft():
    text = subprocess.check_output("whereis geckodriver", shell=True, text=True)
    pattern = r"geckodriver: (?P<path>.*?)\s+"
    path = re.search(pattern, text).group("path")

    service = webdriver.FirefoxService(path)
    browser = webdriver.Firefox(service=service)
    # browser.get('http://selenium.dev/')

    browser.get("https://codeforces.com/enter")

    handle_element = browser.find_element(By.XPATH, "//input[@id='handleOrEmail']")
    handle_element.clear()
    handle_element.send_keys("")

    password_element = browser.find_element(By.XPATH, "//input[@id='password']")
    password_element.clear()
    password_element.send_keys("")

    submit_element = browser.find_element(By.XPATH, "//input[@class='submit']")
    submit_element.click()

    # "https://codeforces.com/group/CYMPFXi8zA/contest/279284/problem/B"
    problem_info = ProblemInfo(group="CYMPFXi8zA", contest="279284", problem="B")
    submit_link = f"https://codeforces.com/group/{problem_info.group}/contest/{problem_info.contest}/submit"

    browser.get(submit_link)

    # select_element = browser.find_element(By.XPATH, "//select[@name='submittedProblemIndex']")
    # option_element = select_element.find_element(By.XPATH, "//option[@value='B']")

    problem_option_element = browser.find_element(By.XPATH, "//option[@value='B']")
    problem_option_element.click()
    language_option_element = browser.find_element(By.XPATH, "//option[@value='89']")
    language_option_element.click()

    switch_off_editor_element = browser.find_element(
        By.XPATH, "//input[@id='toggleEditorCheckbox']"
    )
    if not switch_off_editor_element.is_selected():
        switch_off_editor_element.click()

    source_code_element = browser.find_element(By.ID, "sourceCodeTextarea")

    submission_file = Path("")
    submission_text = submission_file.open().read()
    source_code_element.send_keys(submission_text)

    # TODO: ensure that submission is unique
    submit_element = browser.find_element(
        By.XPATH, "//input[@id='singlePageSubmitButton']"
    )
    # assert browser.current_url == 'https://codeforces.com/group/CYMPFXi8zA/contest/279284/my'

    browser.refresh()

    # switch_off_editor_element = browser.find_elements(By.CLASS_NAME, "view-source")
    submission_elements = browser.find_elements(By.CLASS_NAME, "highlighted-row")
    submission_element = submission_elements[0]
    submission_id = submission_element.get_attribute("data-submission-id")
    view_source_element = browser.find_element(
        By.XPATH, f"//*[@submissionid='{submission_id}' and @class='view-source']"
    )

    status_element = submission_element.find_element(By.CLASS_NAME, "status-cell")
    status_element.get_attribute("waiting")
    verdict = status_element.text
