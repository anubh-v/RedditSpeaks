# RedditSpeaks - Find out what Reddit is saying

Reddit is a platform for hosting interest or place based communities.

RedditSpeaks is a project about extracting results and relationships from the data available on Reddit.

Problem areas being considered:
- Identifying trends across time in various Reddit communities
- Tracking the popularity of various topics across geospatial boundaries
- Tracking community activity over time

View some results [here](docs/results.md)

## Usage of `cli.py`

To download Reddit submissions from the Pushshift API, run:
`python cli.py <subreddit name> --start <year, month, day> --end <year, month, day> --output <path to output file>`

To extract names from these downloaded submissions, run:
`python cli.py --input <path to input file> --output <path to output file>`

Note: within `Client.py`, there is a 1 second delay between each call to the Pushshift API (to avoid spamming).

### Examples

To download submissions from [r/politics](https://www.reddit.com/r/politics/) 
between 1 March 2019 and 2 March 2019, run: `python cli.py politics --start 2019 3 1 --end 2019 3 2 --output politics.json`

To extract names, run:
`python cli.py names --input politics.json --output names.json`
