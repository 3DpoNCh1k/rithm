from rithm.rithm import rithm


def run_command(args):
    rithm.run_command(args.profile, args.compiler, args.filename, args.local_debug)


def add_run_command(subparsers):
    run = subparsers.add_parser("run")
    run.add_argument("filename")
    run.add_argument("profile")
    run.add_argument("local_debug", nargs="?", default=False)
    run.add_argument("--compiler", choices=["g++", "clang"], default="g++")
    run.set_defaults(cmd=run_command)
