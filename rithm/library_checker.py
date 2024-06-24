import subprocess
from .config import LIBRARY_CHECKER_DIRECTORY


def generate_testcases(checker_path):
    generator = LIBRARY_CHECKER_DIRECTORY / "generate.py"
    test_info = checker_path / "info.toml"
    cmd = f"{generator} {test_info}"
    subprocess.check_call(cmd, shell=True)


class LibraryChecker:
    pass