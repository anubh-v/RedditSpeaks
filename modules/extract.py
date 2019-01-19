from psaw import PushshiftAPI
import datetime as dt
import nltk
import json
from tokenizer import tokenize

api = PushshiftAPI()

start = int(dt.datetime(2019, 1, 1).timestamp())
end = int(dt.datetime(2019, 1, 19).timestamp())


gen = api.search_submissions(after=start, before=end, subreddit='singapore')
results = list(gen)

print(len(results))

data = {}
data['titles'] = []

for result in results:
    print(result.title)
    data['titles'].extend(tokenize(result.title))
    print(result.selftext)

freq = nltk.FreqDist(data['titles'])
print(freq.most_common(50))

with open('results.json', 'w') as outfile:
    json.dump(data, outfile)
