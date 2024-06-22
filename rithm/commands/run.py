import os
import subprocess

from rithm.config import load_config


def run_command(args):
    filename = args.filename
    profile = args.profile
    dbg = bool(args.local_debug)
    compiler = args.compiler

    assert filename[-4:] == ".cpp"
    executable = filename[:-4] + ".exe"

    config = load_config()
    config = config["compiler"][compiler]
    std = config["std"]
    always_flags = config["always"]
    profile_flags = config["profiles"][profile]
    debug_flags = config["localDebug"] if dbg else ""

    cmd = f"{compiler} --std={std} {always_flags} {profile_flags} {debug_flags}"
    cmd += f" -o {executable} {filename}"

    if os.path.exists(executable):
        os.remove(executable)

    res = subprocess.run(cmd, shell=True, check=True)
    assert res.returncode == 0
    res = subprocess.run(executable, shell=True, check=True)
    assert res.returncode == 0
