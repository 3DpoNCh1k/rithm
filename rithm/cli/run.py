from rithm.rithm import rithm

def run_command(args):
    filename = args.filename
    profile = args.profile
    local_debug = bool(args.local_debug)
    compiler = args.compiler
    assert filename[-4:] == ".cpp"

    rithm.run_command(profile, compiler, filename, local_debug)
    

def add_run_command(subparsers):
    run = subparsers.add_parser("run")
    run.add_argument("filename")
    run.add_argument("profile")
    run.add_argument("local_debug", nargs="?", default=False)
    run.add_argument("--compiler", choices=["g++", "clang"], default="g++")
    run.set_defaults(cmd=run_command)
