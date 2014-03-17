import narwal
import feedparser
import time
import traceback
from datetime import datetime
from sys import exit

user_name = "bringer-of-news" # will prompt at start if set to None
password = None # will prompt at run if set to None
subreddit = "testing_bot"
feeds = ["http://boards.4chan.org/v/index.rss"]
pause_time = 20 # seconds to wait before we check feeds again
log_file = "./bringer-of-news.log"

def log(f, s):
    now = datetime.now()
    print "[%s] %s" % (now.ctime(), s)
    print >>f, "[%s] %s" % (now.ctime(), s)
    f.flush()

if user_name is None:
    print "Username:",
    user_name = raw_input()

if password is None:
    print "Password for %s:" % user_name,
    password = raw_input()

def main(loghandle):
    try:
        session = narwal.connect(user_name, password, "User-Agent: Fighting Game RSS Aggregator")
    except narwal.exceptions.LoginFail:
        log(loghandle, "Couldn't log in.")
        exit(0)

    log(loghandle, "Connected as %s." % user_name)

    last_checked = datetime.utcnow()

    while True:
        log(loghandle, "Checking for new feeds.")
            
        for feed in feeds:
            d = feedparser.parse(feed)
            if d.bozo is 1:
                log(loghandle, "Malformed feed! URL: %s" % feed)
                break
            for entry in d.entries:
                # skip entries with empty fields, as that problem popped up recently
                if not entry.title or entry.link: break

                # if the entry is newer than when we last checked ...
                if entry.published_parsed >= last_checked.timetuple():
                    try:
                        link = session.submit_link(subreddit, entry.title, entry.link, False)
                        log(loghandle, "Posted \"%s\"" % link)
                    except narwal.exceptions.PostError, e:
                        log(loghandle, "Couldn't submit link: %s (%s)" % (entry.title, e)
                        
        last_checked = datetime.utcnow()
        log(loghandle, "Sleeping %d second(s)." % pause_time)
        time.sleep(pause_time)

if __name__ == "__main__":
    with open(log_file, 'a') as f:
        try: main(f)
        except KeyboardInterrupt: log(f, "\nShutting down.")
        except:
            log(f, "Shutdown because of error!\n%s" % traceback.format_exc())
            raise
