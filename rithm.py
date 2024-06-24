#!/usr/bin/env python3

import argparse
import sys
import traceback

from rithm.cli import *


def main():
    parser = argparse.ArgumentParser(prog="rithm")

    subparsers = parser.add_subparsers()

    add_run_command(subparsers)
    add_clean_command(subparsers)
    add_prepare_submission_command(subparsers)
    add_check_dependencies_command(subparsers)
    add_check_all_command(subparsers)
    add_test_command(subparsers)
    add_build_command(subparsers)

    args = parser.parse_args()

    if "cmd" not in args:
        parser.print_help()
        sys.exit(2)

    try:
        args.cmd(args)
    except Exception as e:
        print(e)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
