from functools import reduce
import json
import nltk


def trim(submission):

    # Create a new list of submissions, keeping only required fields
    return dict(title=submission['title'], id=submission['id'])


def extract_names(submission):
    name_extraction_helper(submission)

    """
    Create a field for comments,
    and treat title as a comment (for simplicity)
    """
    submission['comments'] = [submission['title']]
    del submission['title']

    submission['ids'] = [submission['id']]
    del submission['id']

    return submission


def perform_name_extraction(submissions, output_path):

    trimmed_submissions = map(trim, submissions)
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

    def does_not_have_short_names(
        submission): return len(submission['name']) > 3
    cleaned_submissions = filter(does_not_have_short_names,
                                 unpacked_named_submissions)

    sorted_submissions = sorted(cleaned_submissions,
                                key=lambda submission: submission['name'])

    """
    for sub in sorted_submissions:
      print(sub['ids'])
    """

    sorted_submissions[0] = [sorted_submissions[0]]

    """
    Merge named submissions that are associated with the same name.
    """
    flattened = reduce(flatten, sorted_submissions)
    """
    Sort named submissions, in order of number of comments associated with
    each name.
    """

    flattened.sort(
        key=lambda named_submission: len(named_submission['comments']),
        reverse=True)

    with open(output_path, 'w') as outfile:
        json.dump(flattened, outfile, indent=1)


def flatten(uniq_data_so_far, next_data):
    data_to_be_compared = uniq_data_so_far[-1]

    if data_to_be_compared['name'] != next_data['name']:
        uniq_data_so_far.append(next_data)
        return uniq_data_so_far
    else:
        data_to_be_compared['comments'].append(next_data['comments'][0])
        data_to_be_compared['ids'].append(next_data['ids'][0])
        return uniq_data_so_far


def name_extraction_helper(data):

    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(data['title'])
    tagged_tokens = nltk.pos_tag(tokens)

    completed_names = []
    current_name = []

    # count = 0

    for i in tagged_tokens:

        if i[1] == 'NNP':

            if len(current_name) == 0:
                current_name.append(i[0].lower())

            elif len(current_name) != 0:
                current_name[0] = current_name[0] + " " + i[0].lower()

                completed_names.append(current_name[0])
                current_name = []

        else:
            if current_name:
                completed_names.append(current_name[0])

                current_name = []

    data['names'] = completed_names
