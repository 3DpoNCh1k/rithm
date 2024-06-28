#!/usr/bin/env python3

import os
from pathlib import Path

RITHM_DIRECTORY = Path(os.path.realpath(__file__)).parent
BIN_DIRECTORY = RITHM_DIRECTORY / "bin"

RUN_SCRIPT_FILE = BIN_DIRECTORY / "rithm"
RUN_SCRIPT_TEXT = f"""#!/bin/sh
{RITHM_DIRECTORY}/rithm.py $@
"""

ACTIVATION_SCRIPT_FILE = RITHM_DIRECTORY / "activation.sh"
ACTIVATION_SCRIPT_TEXT = f"""
export PATH={BIN_DIRECTORY}:$PATH

complete -W "{{rithm_commands}}" rithm
"""

PROFILE_SCRIPT_TEXT = f"""
# rithm
if [ -f "{ACTIVATION_SCRIPT_FILE}" ]; then source {ACTIVATION_SCRIPT_FILE}; fi
"""


def create_run_script():
    BIN_DIRECTORY.mkdir(exist_ok=True)
    open(RUN_SCRIPT_FILE, "w").write(RUN_SCRIPT_TEXT)
    os.chmod(RUN_SCRIPT_FILE, 0o755)


def create_activation_script():
    commands = (RITHM_DIRECTORY / "commands.txt").open().read().split()
    open(ACTIVATION_SCRIPT_FILE, "w").write(
        ACTIVATION_SCRIPT_TEXT.format(rithm_commands=" ".join(commands))
    )


def update_profile():
    profile = Path.home() / ".bashrc"
    with open(profile) as file:
        if file.read().find(PROFILE_SCRIPT_TEXT):
            return

    with open(profile, "a") as file:
        file.write(PROFILE_SCRIPT_TEXT)


def main():
    create_run_script()
    create_activation_script()
    update_profile()


if __name__ == "__main__":
    main()
