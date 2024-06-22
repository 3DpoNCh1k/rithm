import os
from pathlib import Path
import subprocess

from rithm.graph import *


def check_dependencies_command(args):
    path = Path(args.filename)
    g = create_graph(path)
    result, cycle = has_cycle(g)
    if result:
        print(f"Found cycle: {cycle}")
        sys.exit(1)
    print("Success!")


def check_all_command(args):
    print("check_all_command")
    path = Path(args.path)
    cpp_extensions = ["cpp", "hpp", "h"]
    for ext in cpp_extensions:
        for file_path in path.glob(f"**/*.{ext}"):
            print(file_path)
            # continue
            g = create_graph(file_path)
            result, cycle = has_cycle(g)
            if result:
                print(f"Found cycle: {cycle}")
                sys.exit(1)

    check_pragma(path)
    print("Success!")


def has_pragma(path):
    return path.open().read().startswith("#pragma once")


def check_pragma(path):
    header_extensions = ["hpp", "h"]
    for ext in header_extensions:
        for file_path in path.glob(f"**/*.{ext}"):
            if not has_pragma(file_path):
                print(f"File {file_path} does not has #pragma once")
                sys.exit(1)

    print("Success!")
