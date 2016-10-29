#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# https://www.dataquest.io/blog/streaming-data-python/
import time
import tweepy
import json
import csv
from getpass import getpass
from textwrap import TextWrapper

# Keywords
track_Michigan = ['GoBlue', 'Ann Arbor', 'UMich', 'Michigan Wolverines', 'BigHouse', 'University of Michigan', 'Duderstadt', 'Yost arena', 'Crisler Center', 'Zingermann']
import csv
w = open("result.csv", "w")
# extract a row of info into csv from status
# Features: user_id, source_id if RT, content, location of user, # of RT, # of followers, # of followees, # timestamp, tweet ID
def writeAsJSON(status):
    rowInfo = {}
    rowInfo['content'] = status.text
    rowInfo['user_id'] = status.author.id
    rowInfo['user_follower_count'] = status.author.followers_count
    rowInfo['user_location'] = status.author.location
    rowInfo['retweet_count'] = status.retweet_count
    rowInfo['timestamp'] = status.timestamp_ms
    if status.retweeted_status:
        rowInfo['retweeted_author_id'] = status.retweeted_status.author.id
        rowInfo['retweeted_author_followers_count'] = status.retweeted_status.author.followers_count
        rowInfo['retweeted_author_location'] = status.retweeted_status.author.location
        rowInfo['retweeted_favorite_count'] = status.retweeted_status.favorite_count
    json.dump(rowInfo, w)

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print self.status_wrapper.fill(status.text)
            #json.dump(rowInfo, w)
            writeAsJSON(status)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():
    access_token = "308609794-UnsFrbl4fcBQsOzbG5sqliFMKowhOlzRmLHVeBdp"
    access_token_secret = "BwjfaD1QgiF0wEzMdyBDsLLEnYXeXLpLqgVcru4oU9QLB"
    consumer_key = "Tzui94xupQIdChpAD7shh6DVo"
    consumer_secret = "uMRrB7tH7YHgANboYa3wB1U0HHGm2g51j9Aj7QG9XVZnLgRlv9"

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = raw_input('Mode? [sample/filter] ')
        if mode in valid_modes:
            break
        print 'Invalid mode! Try again.'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        track_list = track_Michigan
        print track_list
        stream.filter([], track_list, languages=['en'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
        w.close()