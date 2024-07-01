import os
import shutil
import subprocess
from pathlib import Path

from rithm.utils import get_files_from_directory

STRESS_DIRECTORY = Path(os.path.realpath(__file__)).parent


class Stress:
    def __init__(self):
        pass

    def create(self):
        current_path = Path(".")
        stress_path = current_path / "stress"
        stress_path.mkdir()
        for file in get_files_from_directory(self.templates_path):
            shutil.copy(file, stress_path)

    def run(self):
        current_path = Path(".").absolute()
        stress_path = current_path / "stress"
        tester = stress_path / "tester.py"
        assert tester.exists()
        subprocess.check_call(f"python {tester}", shell=True)

    @property
    def templates_path(self):
        return STRESS_DIRECTORY / "templates"
