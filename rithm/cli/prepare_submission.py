from pathlib import Path

from rithm.rithm import rithm


def prepare_submission_command(args):
    rithm.prepare_submission_command(args.filename)


def add_prepare_submission_command(subparsers):
    prepare_submission = subparsers.add_parser("prepare-submission")
    prepare_submission.add_argument("filename")
    prepare_submission.set_defaults(cmd=prepare_submission_command)
