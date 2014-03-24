import feedparser
import json
import sys
import io
from datetime import datetime, timedelta
import calendar
from jinja2 import Environment, FileSystemLoader


def read_channel(channel):
    links = []
    feedurl = "http://gdata.youtube.com/feeds/base/users/{}/uploads".format(channel["title"])
    d = feedparser.parse(feedurl)

    for entry in d.entries:
        if not(entry.title) or not(entry.link):
            print "Skipping entry from '{}' because of empty fields.".format(channel["title"])
            continue

        now = datetime.utcnow()
        if entry.published_parsed >= (now - timedelta(weeks=1)).timetuple():
            links.append(u"[{}]({})".format(entry.title, entry.link))

    if channel["comment"]:
        return {"title": channel["title"], "comment": channel["comment"], "links": links}
    else:
        return {"title": channel["title"], "links": links}
        

def main(config):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(config["template"])
    channels = config["channels"]

    today = datetime.today()
    datestring = "{} {}".format(calendar.month_name[today.month], today.day)

    with io.open(config["outfile"], 'w') as f:
        f.write(template.render(channels=[read_channel(c) for c in channels],
            datestring=datestring))

if __name__ == "__main__":
    try:
        config_file = sys.argv[1]
    except IndexError:
        config_file = "config.json"

    with io.open(config_file) as f:
        try:
            config = json.load(f)
        except ValueError:
            print "Something is wrong with your config: %s" % config_file
            sys.exit(0)

    main(config["weekly-videos"])
