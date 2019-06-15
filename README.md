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
pip3 install Flask==1.0.2 Flask-Cors==3.0.7
pip3 install psaw
pip3 install nltk
python3 run_app.py
```

### client side(run on port 3000)
```sh
cd client
npm install
npm run start
```


