from psaw import PushshiftAPI
import datetime as dt
import nltk
import json
from modules.tokenizer import tokenize
from modules.objectify import make_object_array


def extract_data():
    api = PushshiftAPI()

    start = int(dt.datetime(2018, 6, 1).timestamp())
    end = int(dt.datetime(2018, 6, 30).timestamp())

    gen = api.search_submissions(
        after=start, before=end, subreddit='singapore')
    results = list(gen)

    print(len(results))

    data = {}
    data['titles'] = []

    for result in results:
        data['titles'].extend(tokenize(result.title))

    freq = nltk.FreqDist(data['titles'])

    print(freq.most_common(50))
    return make_object_array(freq.most_common(50))
