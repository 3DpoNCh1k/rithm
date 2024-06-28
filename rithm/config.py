import json
import os
import sys
from pathlib import Path

# TODO: handle it better
try:
    ALGO_PATH = Path(os.environ["ALGO_PATH"])
    assert ALGO_PATH.is_absolute()
    assert ALGO_PATH.exists()
except KeyError:
    print("Set ALGO_PATH environment variable that points to algo library")
    sys.exit(1)

CONFIG_DIRECTORY = Path(os.path.realpath(__file__)).parent
RITHM_DIRECTORY = CONFIG_DIRECTORY.parent
LIBRARY_CHECKER_DIRECTORY = RITHM_DIRECTORY / "library-checker-problems"


def load_config():
    return json.load(open(RITHM_DIRECTORY / "config.json"))
