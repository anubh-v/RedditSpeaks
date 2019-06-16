[![Build Status](https://travis-ci.org/Abstraction-Support-Group/RedditSpeaks.svg?branch=master)](https://travis-ci.org/Abstraction-Support-Group/RedditSpeaks)

# RedditSpeaks - Find out what Reddit is saying

Reddit is a platform for hosting interest or place based communities.

RedditSpeaks is a project about extracting results and relationships from the data available on Reddit.

Problem areas being considered:
- Identifying trends across time in various Reddit communities
- Tracking the popularity of various topics across geospatial boundaries
- Tracking community activity over time

View some results [here](docs/results.md)


## Run

### server side(run on port 5000(consider making this dynamic))
```sh
cd server
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 run_app.py
```

### client side(run on port 3000)
```sh
cd client
npm install
npm run start
```


## Usage of `cli.py`

`cli.py` is meant for performing NLP tasks from command line.

Usage syntax: `python cli.py <command> <arguments>`

Current commands:
1. `pull` - download Reddit submissions and save to a file.
2. `names` - extract names from Reddit submissions, loaded from a file.

To download Reddit submissions, run:
`python cli.py pull <subreddit name> --start <year, month, day> --end <year, month, day> --output <path to output file>`

To extract names from these downloaded submissions, run:
`python cli.py names --input <path to input file> --output <path to output file>`

Note: Within `Client.py`, the Reddit data is obtained from the [Pushshift API](https://github.com/pushshift/api)
and there is a 1 second delay between each call to the Pushshift API (to avoid spamming).

### Examples

To download submissions from [r/politics](https://www.reddit.com/r/politics/) 
between 1 March 2019 and 2 March 2019, run: `python cli.py pull politics --start 2019 3 1 --end 2019 3 2 --output politics.json`

To extract names, run:
`python cli.py names --input politics.json --output names.json`

In this example, the following are the top 10 extracted names:

| Name       | Number of associated titles | 
| ------------- |-----:|
| trump |267|
| michael cohen|100|
| cohen | 68|
|kim jong| 44 |
|house| 39|
|otto warmbier| 35|
|north korea| 34|
|donald trump|27|
|jay inslee|23|
|senate|23|

