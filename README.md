[![Build Status](https://travis-ci.org/anubh-v/RedditSpeaks.svg?branch=master)](https://travis-ci.org/anubh-v/RedditSpeaks)

# RedditSpeaks - Find out what Reddit is saying

RedditSpeaks is a project about extracting information from news articles shared on Reddit.

Currently, RedditSpeaks can identify the most common names mentioned in news
headlines on Reddit.

View some results [here](docs/results.md)

## Install

Preferably, use a new Python environment.

```
pip install -r requirements.txt
```

## Quick start

To download submissions from [r/politics](https://www.reddit.com/r/politics/) 
between 1 March 2019 and 2 March 2019, run: 
```
python cli.py pull politics --start 2019 3 1 --end 2019 3 2 --output politics.json`
```

Next, to extract names, run:
```
python cli.py names --input politics.json --output names.json`
```

Next, to generate a wordlcoud, run:
```
python cli.py view --input names.json`
```
Below is the word cloud generated for this time period:

![Word cloud from a Reddit forum about US news, over the first days of March 2018](docs/visuals/politicsEarlyMarch2018.jpg)

## Usage

`cli.py` is meant for performing NLP tasks from command line.

Usage syntax: `python cli.py <command> <arguments>`

Current commands:
1. `pull` - download Reddit submissions and save to a file.
2. `names` - extract names from Reddit submissions, loaded from a file.
3. `view` - generate a wordcloud displaying the extracted names


To download Reddit submissions, run:
```
python cli.py pull <subreddit name> --start <year, month, day> --end <year, month, day> --output <path to output file>`
```

To extract names from these downloaded submissions, run:
```
python cli.py names --input <path to input file> --output <path to output file>`
```
To generate a wordcloud displaying these extracted names, run:
```
python cli.py view --input <path to json file containing extracted names>
```
