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

    # remove unnecessary fields from every submission
    trimmed_submissions = map(trim, submissions)

    # identify the names present in each submission
    # a submission could be associated with more than 1 name
    with_extracted_names = map(extract_names, trimmed_submissions)

    # remove submissions with no identified names
    named_submissions = filter(has_name, with_extracted_names)

    """
    For submissions with multiple names, create copies of the submission with
    1 name each
    """
    def unpack(submission, name):
        return dict(title=submission['title'],
                    id=submission['id'],
                    name=name)

    unpacked_named_submissions = (unpack(submission, name)
                                  for submission in named_submissions
                                  for name in submission['names'])

    """
    Remove submissions associated with very short names.
    These names are unlikely to be meaningful.
    """

    cleaned_submissions = filter(does_not_have_short_names,
                                 unpacked_named_submissions)

    """
    Sort submissions with respect to their names (i.e. sort using the
    submission's name as the key)
    """
    sorted_submissions = sorted(cleaned_submissions,
                                key=lambda submission: submission['name'])

    """
    Group together named submissions which are associated with the same name.
    
    """
    # Prepare named submissions for grouping
    ready_to_be_grouped = [prepare_for_grouping(submission)
                           for submission in sorted_submissions]

    ready_to_be_grouped[0] = list(ready_to_be_grouped[0])

    grouped = reduce(group, ready_to_be_grouped)

    """
    Sort named submissions, in order of number of titles associated with
    each name.
    """
    grouped.sort(
        key=lambda named_submission: len(named_submission['titles']),
        reverse=True)

    """
    Write sorted named submissions to file.
    """
    with open(output_path, 'w') as outfile:
        json.dump(flattened, outfile, indent=1)


def extract_names(submission):
    submission['names'] = naive_name_detector(submission['title'])
    return submission


def prepare_for_grouping(submission):
    return dict(titles=list(submission['title']),
                ids=list(submission['id']),
                name=submission['name'])


def group(uniq_data_so_far, next_data):
    data_to_be_compared = uniq_data_so_far[-1]

    if data_to_be_compared['name'] != next_data['name']:
        uniq_data_so_far.append(next_data)
        return uniq_data_so_far
    else:
        data_to_be_compared['titles'].append(next_data['titles'][0])
        data_to_be_compared['ids'].append(next_data['ids'][0])
        return uniq_data_so_far


def trim(submission):
    # Create a new dictionary, keeping only the title and id
    return dict(title=submission['title'],
                id=submission['id'])


def does_not_have_short_names(submission):
    return len(submission['name']) > 3


def has_name(submission):
    return len(submission['names']) != 0
