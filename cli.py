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
import json

from etl import Client, Tasks, Util, WordCloud


def pull_data(context):
    subreddit = context.subreddit
    start_date = list(map(int, context.start))
    end_date = list(map(int, context.end))
    output_path = context.output

    data_store = Client.pull(subreddit, start_date, end_date)
    Client.write(data_store, output_path)


def extract_names(context):
    input_path = context.input
    output_path = context.output

    data_generator = Client.read(input_path)
    Tasks.perform_name_extraction(data_generator, output_path)


def extract_action_phrases(context):
    input_path = context.input
    output_path = context.output

    with open(input_path) as infile:
        data = json.load(infile)

    data_generator = iter(data)

    extracted = Tasks.perform_action_phrase_extraction(data_generator)
    Client.write(extracted, output_path)


def make_local_wordcloud(context):
    names_filepath = context.input
    with open(names_filepath) as infile:
        names_data = json.load(infile)
        frequencies = Util.get_frequencies(names_data)
        WordCloud.make_image(frequencies)


if __name__ == "__main__":
    """
    Create an overall ArgumentParser, which expects the user to specify a
    command (such as "pull" or "names")
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    # The user must specify a command
    subparsers.required = True

    # Create a parser for the "names" command.
    name_command = subparsers.add_parser('names')
    name_command.add_argument('--input', type=str, required=True,
                              help='a path to a file containing \
                                    downloaded reddit data')

    name_command.add_argument('--output', type=str, required=True,
                              help='a location for storing results')

    name_command.set_defaults(handler=extract_names)

    # Create a parser for the "pull" command.
    pull_command = subparsers.add_parser('pull')
    pull_command.add_argument('subreddit', type=str,
                              help="a subreddit's name")

    pull_command.add_argument('--start', nargs="+", type=str, required=True)
    pull_command.add_argument('--end', nargs="+", type=str, required=True)
    pull_command.add_argument('--output', type=str, required=True)
    pull_command.set_defaults(handler=pull_data)

    # Create parser for the "view" command.
    view_command = subparsers.add_parser('view')
    view_command.add_argument('--input', type=str, required=True,
                              help='a path to the file containing \
                                    extracted names')

    view_command.set_defaults(handler=make_local_wordcloud)

    """
    Parse the user input into a "context" object that encapsulates
    the arguments and options specified in the input
    """
    context = parser.parse_args()
    # Run the handler function associated with the user's chosen command
    context.handler(context)
