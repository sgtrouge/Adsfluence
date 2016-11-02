# -*- coding: utf-8 -*-
import oauth2
import json
from pprint import pprint

# Find friends of a person.
# TODO: Implement waiting so we don't get rate limit error
def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    consumer = oauth2.Consumer(key='', secret='')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    cursor = -1
    while cursor != 0:
        cursor_url = url + '&cursor='+ str(cursor)
        resp, content = client.request( cursor_url, method=http_method, body=post_body, headers=http_headers)
        tmp = json.loads(content)
        cursor = tmp['next_cursor']
        print len(tmp['ids'])

    return content

# find who a specific user follows. Change the screen name below
home_timeline = oauth_req( 'https://api.twitter.com/1.1/friends/ids.json?screen_name=JoeyBats19', '', '' )
