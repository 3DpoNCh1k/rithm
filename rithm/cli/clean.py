from rithm.rithm import rithm

def clean_command(args):
    rithm.clean_command(args.path)

def add_clean_command(subparsers):
    clean = subparsers.add_parser("clean")
    clean.add_argument("path")
    clean.set_defaults(cmd=clean_command)