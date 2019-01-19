from psaw import PushshiftAPI
import datetime as dt
import json

api = PushshiftAPI()

start = int(dt.datetime(2019, 1, 1).timestamp())
end = int(dt.datetime(2019, 1, 2).timestamp())


gen = api.search_submissions(after=start, before=end, subreddit='worldnews')
results = list(gen)

print(len(results))

data = {}
data['titles'] = []

for result in results:
  print(result.title)
  data['titles'].append(result.title)
  print(result.selftext)

with open('results.json', 'w') as outfile:
    json.dump(data, outfile)


