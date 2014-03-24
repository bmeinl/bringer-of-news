import json
import narwal
import feedparser
import time
import traceback
from datetime import datetime
import sys

def log(f, s):
    now = datetime.now()
    print "[%s] %s" % (now.ctime(), s)
    print >>f, "[%s] %s" % (now.ctime(), s)
    f.flush()

def main(loghandle, config):
    try:
        session = narwal.connect(config["user_name"], config["password"], "User-Agent: Fighting Game RSS Aggregator")
    except narwal.exceptions.LoginFail:
        log(loghandle, "Couldn't log in.")
        sys.exit(0)

    log(loghandle, "Connected as %s." % config["user_name"])

    last_checked = datetime.utcnow()

    while True:
        log(loghandle, "Checking for new feeds.")
            
        for feed in config["feeds"]:
            d = feedparser.parse(feed)
            if d.bozo is 1:
                log(loghandle, "Malformed feed! URL: %s" % feed)
                break
            for entry in d.entries:
                # skip entries with empty fields, as that problem popped up recently
                if not(entry.title) or not(entry.link):
                        print "Skipping entry from '%s' because of empty fields." % feed
                        break

                # if the entry is newer than when we last checked ...
                if entry.published_parsed >= last_checked.timetuple():
                    try:
                        link = session.submit_link(config["subreddit"], entry.title, entry.link, False)
                        log(loghandle, "Posted \"%s\"" % link)
                    except narwal.exceptions.PostError, e:
                        log(loghandle, "Couldn't submit link: %s (%s)" % (entry.title, e.errors))
                        
        last_checked = datetime.utcnow()
        log(loghandle, "Sleeping %d second(s)." % config["pause_time"])
        time.sleep(config["pause_time"])

if __name__ == "__main__":
    try:
        config_file = sys.argv[1]
    except IndexError:
        config_file = "config.json"

    with open(config_file, 'r') as f:
        try:
            config = json.load(f)
        except ValueError:
            print "Something is wrong with your config: %s" % config_file
            sys.exit(0)

    with open(config["bringer-of-news"]["log_file"], 'a') as f:
        try: main(f, config["bringer-of-news"])
        except KeyboardInterrupt: log(f, "\nShutting down.")
        except:
            log(f, "Shutdown because of error!\n%s" % traceback.format_exc())
            raise
