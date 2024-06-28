from .problem_info import ProblemInfo


def main_link():
    return "https://codeforces.com"


def login_link():
    return f"{main_link()}/enter"


def profile_link(handle):
    return f"{main_link()}/profile/{handle}"


def submit_link(problem_info: ProblemInfo):
    return f"{main_link()}/group/{problem_info.group}/contest/{problem_info.contest}/submit"


def my_submissions_link(problem_info: ProblemInfo):
    return f"{main_link()}/group/{problem_info.group}/contest/{problem_info.contest}/my"


def get_source_code_link(problem_info: ProblemInfo):
    return f"{main_link()}/group/{problem_info.group}/data/submitSource"
