"""
This module provides a command line interface to download reddit data
and perform NLP tasks on them.

Usage syntax: python cli.py <command> <arguments>

Current commands:
    1. pull - download Reddit submissions and save to a file.
    2. names - extract names from Reddit submissions, loaded from a file.

To download Reddit submissions, run:
python cli.py pull <subreddit name> --start <year, month, day>
--end <year, month, day> --output <path to output file>

To extract names from these downloaded submissions, run:
python cli.py names --input <path to input file> --output <path to output file>

"""

import argparse

from etl import Client, Tasks


def pull(context):
    subreddit = context.subreddit
    start_date = list(map(int, context.start))
    end_date = list(map(int, context.end))
    output_path = context.output

    data_store = Client.pull(subreddit, start_date, end_date)
    Client.write(data_store, output_path)


def names(context):
    input_path = context.input
    output_path = context.output

    data_generator = Client.read(input_path)
    Tasks.perform_name_extraction(data_generator, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    name_command = subparsers.add_parser('names')
    name_command.add_argument('--input', type=str, required=True)
    name_command.add_argument('--output', type=str, required=True)
    name_command.set_defaults(func=names)

    pull_command = subparsers.add_parser('pull')
    pull_command.add_argument('subreddit', type=str)
    pull_command.add_argument('--start', nargs="+", type=str, required=True)
    pull_command.add_argument('--end', nargs="+", type=str, required=True)
    pull_command.add_argument('--output', type=str, required=True)
    pull_command.set_defaults(func=pull)

    context = parser.parse_args()
    context.func(context)
