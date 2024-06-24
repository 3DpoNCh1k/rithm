import json
import os
from pathlib import Path
import sys

def load_config():
    return json.load(open("config.json"))

# TODO: handle it better
try:
    ALGO_PATH = Path(os.environ["ALGO_PATH"])
except KeyError:
    print("Set ALGO_PATH environment variable that points to algo library")
    sys.exit(1)

CONFIG_DIRECTORY = Path(os.path.realpath(__file__)).parent
RITHM_DIRECTORY = CONFIG_DIRECTORY.parent
LIBRARY_CHECKER_DIRECTORY = RITHM_DIRECTORY / "library-checker-problems"
