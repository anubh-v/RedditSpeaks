from psaw import PushshiftAPI
import datetime as dt
api = PushshiftAPI()

start = int(dt.datetime(2019, 1, 1, 0).timestamp())
end = int(dt.datetime(2019, 1, 1, 2).timestamp())


gen = api.search_submissions(after=start, before=end, subreddit='politics')
results = list(gen)

print(len(results))

for result in results:
  print(result.title)
  # print(result.selftext)


