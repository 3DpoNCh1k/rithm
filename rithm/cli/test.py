from rithm.rithm import rithm


def test_command(args):
    rithm.test_command(args.path, args.type)


def add_test_command(subparsers):
    test = subparsers.add_parser("test")
    test.add_argument("path")
    test.add_argument(
        "--type", choices=["tests", "library-checker", "codeforces", "examples"]
    )
    test.set_defaults(cmd=test_command)


def test_task_command(args):
    rithm.test_task_command(args.path, args.testcase)


def add_test_task_command(subparsers):
    test = subparsers.add_parser("test-task")
    test.add_argument("path")
    test.add_argument("--testcase")
    test.set_defaults(cmd=test_task_command)
