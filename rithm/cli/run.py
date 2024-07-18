from rithm.rithm import rithm


def run_command(args):
    rithm.run_command(args.profile, args.filename, args.input)


def add_run_command(subparsers):
    run = subparsers.add_parser("run")
    run.add_argument("profile")
    run.add_argument("filename")
    run.add_argument("input", nargs="?")
    run.set_defaults(cmd=run_command)


def run_examples_command(args):
    rithm.run_examples_command(args.profile, args.filename, args.examples)


def add_run_examples_command(subparsers):
    run_examples = subparsers.add_parser("run-examples")
    run_examples.add_argument("profile")
    run_examples.add_argument("filename")
    run_examples.add_argument("examples")
    run_examples.set_defaults(cmd=run_examples_command)
