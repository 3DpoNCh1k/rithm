from rithm.rithm import rithm


def build_command(args):
    rithm.build_command(args.profile, args.input_file, args.output_file)

def add_build_command(subparsers):
    build = subparsers.add_parser("build")
    build.add_argument("profile")
    build.add_argument("input_file")
    build.add_argument("output_file", nargs='?')
    build.set_defaults(cmd=build_command)
