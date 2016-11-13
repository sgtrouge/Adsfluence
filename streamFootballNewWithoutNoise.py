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
track_Michigan = ['GoBlue', 'UMich', 'Michigan Wolverines', 'BigHouse', 'Big House', 'Football', 'Go Blue', "Maize and Blue", "Wolverines", "Harbaugh","UofM", "UniversityofMichigan", "University of Michigan"]
import csv
w = open("newFootballWithouNoise.txt", "r")
initContent = w.read()
count = len(initContent.split('}{'))
w.close()
w = open("newFootballWithouNoise.txt", "a")


# Read through old user list to ensure we only filter
# tweets of existing user
all_user_id = {}
def readOldUser(filename):
    f = open(filename, 'r')
    global all_user_id
    data = f.read()
    splits = data.split('}{')
    splits[0] = splits[0][1:]
    # For some reason the last one isn't built correctly, need to append ]]
    splits[-1] = splits[-1][:-1] +']]'
    count = 0
    for js in splits:
        jss = '{' + js + '}'
        try:
            tweet_map = json.loads(jss)
            user = tweet_map["user_id"]
            all_user_id[int(user)] = True
            if "retweeted_author_id" in tweet_map:
                retweeted_author_id = tweet_map['retweeted_author_id']
                all_user_id[int(retweeted_author_id)] = True
            count += 1
        except:
            pass
    print len(all_user_id)
    f.close()

# extract a row of info into csv from status
# Features: user_id, source_id if RT, content, location of user, # of RT, # of followers, # of followees, # timestamp, tweet ID
def writeAsJSON(status):
    global count
    print count
    global all_user_id
    if int(status.author.id) not in all_user_id:
        return
    rowInfo = {}
    rowInfo['content'] = status.text
    rowInfo['user_id'] = status.author.id
    rowInfo['user_follower_count'] = status.author.followers_count
    rowInfo['user_location'] = status.author.location
    rowInfo['retweet_count'] = status.retweet_count
    rowInfo['timestamp'] = status.timestamp_ms
    if hasattr(status, 'retweeted_status'):
        if int(status.retweeted_status.author.id) not in all_user_id:
                return
        rowInfo['retweeted_author_id'] = status.retweeted_status.author.id
        rowInfo['retweeted_author_followers_count'] = status.retweeted_status.author.followers_count
        rowInfo['retweeted_author_location'] = status.retweeted_status.author.location
        rowInfo['retweeted_favorite_count'] = status.retweeted_status.favorite_count
    global w
    count = count + 1
    print count
    json.dump(rowInfo, w)

class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print self.status_wrapper.fill(status.text)
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
    readOldUser('resultBackup.txt')
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
