from rithm.rithm import rithm


def check_dependencies_command(args):
    rithm.check_dependencies_command(args.filename)


def check_all_command(args):
    rithm.check_all_command(args.path)


def add_check_dependencies_command(subparsers):
    check_dependencies = subparsers.add_parser("check-dependencies")
    check_dependencies.add_argument("filename")
    check_dependencies.set_defaults(cmd=check_dependencies_command)


def add_check_all_command(subparsers):
    check_all = subparsers.add_parser("check-all")
    check_all.add_argument("path")
    check_all.set_defaults(cmd=check_all_command)
