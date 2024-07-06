from rithm.rithm import rithm


def run_command(args):
    rithm.run_command(args.profile, args.filename, args.input)


def add_run_command(subparsers):
    run = subparsers.add_parser("run")
    run.add_argument("profile")
    run.add_argument("filename")
    run.add_argument("input", nargs="?")
    run.set_defaults(cmd=run_command)
