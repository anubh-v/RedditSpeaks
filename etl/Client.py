"""
This module provides methods to download, read and write Reddit data.

Downloading is done using the Pushshift API.
"""

from datetime import datetime
import json
import requests
import time


def pull(subreddit, start_date, end_date):
    """
    This generator function downloads Reddit submissions from Pushshift.
    Starting from the a given date, this function yields the next available
    submission (as a Python dictionary), until the specified end date is
    reached.

    :param subreddit: a string representing the subreddit name
    :param start_date: a list of integers representing the starting date
    :param end_date: a list of integers representing the end date
    :yield the next submission (as a Python dictionary)

    Example:
    To download submissions from r/politics, dated between 1st March 2019,
    and 5th March 2019, set the arguments as:

    - subreddit = "politics"
    - start_date = [2019, 3, 1]
    - end_date = [2019, 3, 5]

    """

    # Convert the given lists into datetime objects
    start = int(datetime(*start_date).timestamp())
    end = int(datetime(*end_date).timestamp())

    # This is the Pushshift API endpoint for searching Reddit submissions
    base_url = "https://api.pushshift.io/reddit/search/submission/?"

    # Define parameters for the HTTP GET request that will be sent to Pushshift
    subreddit_name = "subreddit=" + subreddit
    time_period = "&after=" + str(start) + "&before=" + str(end)
    # Request for up to 500 results
    requested_size = "&size=500"

    """
    Keep requesting for submissions till we have obtained submissions for
    the entire time period specified in the query
    """
    while(start < end):

        query_url = base_url + subreddit_name + time_period + requested_size
        print(query_url)

        raw_response = requests.get(query_url)
        # Response body will be in JSON
        json_response = json.loads(raw_response.text)

        if len(json_response['data']) == 0:
            """
            If there are no results returned in the response, it means there
            are no Reddit submissions in the given time period.
            We can stop searching.
            """
            break
        else:
            """
            If there are results in the response, yield the next submission.
            """
            for data in json_response['data']:
                yield data

        """
        Once all results in response have been iterated through, update the
        time period and make another request to Pushshift.
        """
        time.sleep(1)
        last_submission_time = json_response['data'][-1]['created_utc']

        print("Retrieved till "
              + datetime.utcfromtimestamp(last_submission_time)
              .strftime('%Y-%m-%d %H:%M:%S'))

        start = last_submission_time
        time_period = "&after=" + str(start) + "&before=" + str(end)


def write(data_generator, output_path):
    """
    Given a iterator of Reddit submissions, this method writes the submissions
    to a test file. The submissions are first cached into lists of
    size <cache_size>.
    Each list is then written onto a line in the file.

    :param data_generator: an iterator of Reddit submissions.
    :param output_path: path to a text file
    """
    cache_size = 1000
    cache = []

    count = 0

    # Each cache is appended onto the existing file contents, in a new line.
    with open(output_path, 'a') as outfile:
        for data in data_generator:
            # Add the next submission into the cache
            count += 1
            cache.append(data)

            if len(cache) > cache_size:
                # Once the cache limit is reached, write out the cached
                # submissions.
                outfile.write(json.dumps(cache))
                outfile.write('\n')
                cache = []

        # After iterating through all submissions, the cache may still be
        # partially full. Write out these remaining submissions.
        outfile.write(json.dumps(cache))
        outfile.write('\n')
        print("Written {} submissions in total".format(count))


def read(input_path):
    """
    Given a text file containing Reddit submissions, yield the next submission,
    as a Python dictionary. The method continues to yield the next submission,
    until all submissions in the file have been exhausted.

    The structure of the data in the text file should be similar to the
    structure adopted in the 'write' method.

    :param input_path: path to a text file containing Reddit submissions.
    :yield: the next submission
    """
    count = 0

    with open(input_path, 'r') as infile:
        for line in infile:
            data_store = json.loads(line)
            for data in data_store:
                count += 1
                yield data

    print("Number read = " + str(count))
