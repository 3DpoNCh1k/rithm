from rithm.rithm import rithm


def stress_create_command(args):
    rithm.stress_create_command()


def stress_run_command(args):
    rithm.stress_run_command()


def add_stress_command(subparsers):
    stress = subparsers.add_parser("stress")
    stress_parsers = stress.add_subparsers()
    create = stress_parsers.add_parser("create")
    create.set_defaults(cmd=stress_create_command)

    run = stress_parsers.add_parser("run")
    run.set_defaults(cmd=stress_run_command)
