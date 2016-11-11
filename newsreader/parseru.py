#!/usr/bin/python

# based on http://alvinalexander.com/python/python-script-read-rss-feeds-database

import feedparser
import time
from subprocess import check_output
import sys

feed_name_1 = 'MEDUZA'
url_1 = 'https://meduza.io/rss/all'

# other feed to test if needed
feed_name_2 = 'Reuters'
url_2 = 'http://feeds.reuters.com/Reuters/worldNews?format=xml'

# db to store news
db_1 = '/home/pi/Pimoroni/scrollphat/feed_1.db'
db_2 = '/home/pi/Pimoroni/scrollphat/feed_2.db'
limit = 3 * 3600 * 1000

# function to get the current time
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                ts_as_string = line.split('|', 1)[1]
                ts = long(ts_as_string)
                if current_timestamp - ts > limit:
                    return True
    return False

#
# get the feed data from the url
# 

rss_feeds = [[feed_name_1, url_1, db_1], [feed_name_2, url_2, db_2]]
for row in rss_feeds:
    feed_name = row[0]
    url = row[1]
    db = row[2]

    feed = feedparser.parse(url)

#
#   figure out which posts to print
#
    posts_to_print = []
    posts_to_skip = []

    for post in feed.entries:
# if post is OLD, skip it
# TODO check the time
        title = post.title
        title = title.encode('UTF-8')
        if post_is_in_db_with_old_timestamp(title):
            posts_to_skip.append(title)
        else:
            posts_to_print.append(title)

#
# add all the posts we're going to print to the database with the current timestamp
# (but only if they're not already in there)
#
    f = open(db, 'a')
    for title in posts_to_print:
        if not post_is_in_db(title):
            f.write(title + "|" + str(current_timestamp) + "\n")
    f.close

# piece of code to delete outdated titles
# open db to read lines
    f = open(db,"r")
    lines = f.readlines()
    f.close

# reopen in write mode
    f = open(db,"w")
    for line in lines:
            timestamp_as_string = line.split('|', 1)[1]
            taims = long(timestamp_as_string)
            if current_timestamp - taims < limit:
                 f.write(line)
    f.close

#
# output all of the new posts
#
    count = 1
    blockcount = 1
    for title in posts_to_print:
        if count % 5 == 1:
            print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
            print("-----------------------------------------\n")
            blockcount += 1
        print(title + "\n")
        count += 1
