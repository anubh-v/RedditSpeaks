"""
This module provides methods to perform extract names from Reddit submissions.
"""

from functools import reduce
import json

from etl.Heuristics import naive_name_detector


def perform_name_extraction(submissions, output_path):
    """
    Given an iterator of Reddit submissions, identifies the names present
    and collates the submissions associated with each name.

    The collated submissions are then written to the specified file.

    :param submissions: an iterator of Reddit submissions
    :param output_path:
    """

    def trim(submission):
        # Create a new dictionary, keeping only the title and id field
        return dict(title=submission['title'], id=submission['id'])

    # remove unnecessary fields from every submission
    trimmed_submissions = map(trim, submissions)

    # identify the names present in each submission
    # a submission could be associated with more than 1 name
    with_extracted_names = map(extract_names, trimmed_submissions)

    # remove submissions with no identified names
    def has_name(submission): return len(submission['names']) != 0
    named_submissions = filter(has_name, with_extracted_names)

    """
    For submissions with multiple names, create copies of the submission with
    1 name each
    """
    def unpack(submission, name):
        return dict(comments=list(submission['comments']),
                    ids=list(submission['ids']),
                    name=name)

    unpacked_named_submissions = (unpack(submission, name)
                                  for submission in named_submissions
                                  for name in submission['names'])

    """
    Remove submissions associated with very short names.
    These names are unlikely to be meaningful.
    """

    def does_not_have_short_names(
        submission): return len(submission['name']) > 3

    cleaned_submissions = filter(does_not_have_short_names,
                                 unpacked_named_submissions)

    """
    Sort submissions with respect to their names (i.e. sort using the
    submission's name as the key)
    """
    sorted_submissions = sorted(cleaned_submissions,
                                key=lambda submission: submission['name'])

    """
    Merge named submissions that are associated with the same name.
    """
    sorted_submissions[0] = [sorted_submissions[0]]
    flattened = reduce(flatten, sorted_submissions)

    """
    Sort named submissions, in order of number of comments associated with
    each name.
    """
    flattened.sort(
        key=lambda named_submission: len(named_submission['comments']),
        reverse=True)

    """
    Write sorted named submissions to file.
    """
    with open(output_path, 'w') as outfile:
        json.dump(flattened, outfile, indent=1)


def extract_names(submission):
    submission['names'] = naive_name_detector(submission['title'])

    """
    Create a field for comments,
    and treat title as a comment (for simplicity)
    """
    submission['comments'] = [submission['title']]
    del submission['title']

    submission['ids'] = [submission['id']]
    del submission['id']

    return submission


def flatten(uniq_data_so_far, next_data):
    data_to_be_compared = uniq_data_so_far[-1]

    if data_to_be_compared['name'] != next_data['name']:
        uniq_data_so_far.append(next_data)
        return uniq_data_so_far
    else:
        data_to_be_compared['comments'].append(next_data['comments'][0])
        data_to_be_compared['ids'].append(next_data['ids'][0])
        return uniq_data_so_far
