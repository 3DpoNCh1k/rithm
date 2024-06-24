import os
import re


def clean_command(args):
    path = args.path
    patterns = [".*\.exe$", ".*\.exp$", ".*\.lib$", ".*\.pdb$"]
    for path, _, filenames in os.walk(path):
        to_remove = filter(
            lambda filename: any(re.match(pattern, filename) for pattern in patterns),
            filenames,
        )
        for filename in to_remove:
            os.remove(path + os.sep + filename)


def add_clean_command(subparsers):
    clean = subparsers.add_parser("clean")
    clean.add_argument("path")
    clean.set_defaults(cmd=clean_command)