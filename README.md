# Overview

Two quick & (very) dirty scripts to help updating a subreddit from RSS feeds.  
Both scripts are configured via JSON file that you optionally specify as command-line parameter.


## bringer-of-news.py

Continuously checks feeds and submits new entries to a subreddit.
Default config file is `config.json`.  
    Usage: bringer-of-news.py [config]


## weekly-videos.py

Aggregates videos of YouTube channels into a single, ready to submit MarkDown file.
Default config file is `config.json`.  
    Usage: weekly-videos.py [config]


---

## Dependencies

* [Narwal](https://github.com/larryng/narwal)
* [Feedparser](http://tf2dingalings.com/sound/details/553)
* [Jinja2](http://jinja.pocoo.org/)
