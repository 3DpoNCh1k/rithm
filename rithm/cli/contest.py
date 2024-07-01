from rithm.rithm import rithm


def contest_create_command(args):
    rithm.contest_create_command(args.problems)


def add_contest_command(subparsers):
    contest = subparsers.add_parser("contest")
    contest_parsers = contest.add_subparsers()
    create = contest_parsers.add_parser("create")
    create.add_argument("problems", nargs="+")
    create.set_defaults(cmd=contest_create_command)
