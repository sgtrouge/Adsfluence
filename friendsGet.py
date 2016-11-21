# -*- coding: utf-8 -*-
import oauth2
import time
import json
from pprint import pprint

# TODO: Integrate with a list of users to get follower graph.
def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    consumer = oauth2.Consumer(key='Tzui94xupQIdChpAD7shh6DVo', secret='uMRrB7tH7YHgANboYa3wB1U0HHGm2g51j9Aj7QG9XVZnLgRlv9')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    cursor = -1
    while cursor != 0:
        try:
            cursor_url = url + '&cursor='+ str(cursor)
            resp, content = client.request( cursor_url, method=http_method, body=post_body, headers=http_headers)
            tmp = json.loads(content)
            cursor = tmp['next_cursor']
            print len(tmp['ids'])
        except:
            waitTime = 15
            print "Rate limit exceeded, waiting for " + str(waitTime) + " minutes"
            time.sleep(60*waitTime)

    return content

# find who a specific user follows. Change the screen name below
home_timeline = oauth_req( 'https://api.twitter.com/1.1/friends/ids.json?screen_name=JoeyBats19', '308609794-UnsFrbl4fcBQsOzbG5sqliFMKowhOlzRmLHVeBdp', 'BwjfaD1QgiF0wEzMdyBDsLLEnYXeXLpLqgVcru4oU9QLB' )
