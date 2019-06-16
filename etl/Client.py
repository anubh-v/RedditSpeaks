from datetime import datetime
import json
import requests
import time


def pull(subreddit, start_date, end_date):

    start = int(datetime(*start_date).timestamp())
    end = int(datetime(*end_date).timestamp())

    base_url = "https://api.pushshift.io/reddit/search/submission/?"

    subreddit_query = "subreddit=" + subreddit
    time_query = "&after=" + str(start) + "&before=" + str(end)
    size_query = "&size=500"

    while(start < end):

        query_url = base_url + subreddit_query + time_query + size_query
        print(query_url)

        raw_response = requests.get(query_url)
        json_response = json.loads(raw_response.text)

        if (len(json_response['data']) == 0):
            break
        else:
            for data in json_response['data']:
                yield data

        time.sleep(1)
        last_submission_time = json_response['data'][-1]['created_utc']

        print("Retrieved till "
              + datetime.utcfromtimestamp(last_submission_time)
              .strftime('%Y-%m-%d %H:%M:%S'))

        start = last_submission_time
        time_query = "&after=" + str(start) + "&before=" + str(end)


def write(data_generator, output_path):

    cache_size = 1000
    cache = []

    count = 0

    with open(output_path, 'a') as outfile:
        for data in data_generator:
            count += 1
            cache.append(data)

            if len(cache) > cache_size:
                outfile.write(json.dumps(cache))
                outfile.write('\n')
                cache = []

        outfile.write(json.dumps(cache))
        outfile.write('\n')
        print("Written {} submissions in total".format(count))


def read(input_path):

    count = 0

    with open(input_path, 'r') as infile:
        for line in infile:
            data_store = json.loads(line)
            for data in data_store:
                count += 1
                yield data

    print("Number read = " + str(count))
