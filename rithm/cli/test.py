from rithm.rithm import rithm


def test_command(args):
    rithm.test_command(args.path)
    

def add_test_command(subparsers):
    test = subparsers.add_parser("test")
    test.add_argument("path")
    test.set_defaults(cmd=test_command)