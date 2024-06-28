import json

from .config import RITHM_DIRECTORY


def load_secrets():
    return json.load(open(RITHM_DIRECTORY / "secrets.json"))
