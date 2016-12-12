import oauth2
import time
import json
from pprint import pprint
from django.utils.encoding import smart_str
import pickle
import csv
w = open("result_eric.csv", "w")

# TODO: Integrate with a list of users to get follower graph.
def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
	consumer = oauth2.Consumer(key='rtSAieJdzAhsALalsFdEU7Xup', secret=	'5q3f3MzZyV9wZVc9IeqZxFiO7l9S6jzFD1Ta4kkVuu9aWTtzf4')
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer, token)
	cursor = -1
	t = 0
	while cursor != 0:
		try:
			cursor_url = url + '&cursor='+ str(cursor)
			resp, content = client.request( cursor_url, method=http_method, body=post_body, headers=http_headers)
			tmp = json.loads(content)
			cursor = tmp['next_cursor']
			print (len(tmp['ids']))
		except:
			waitTime = 15
			print ("Rate limit exceeded, waiting for " + str(waitTime) + " minutes",t)
			t +=1
			if t>1:
				content = []
				break
			time.sleep(60*waitTime)

	return content


json_data = open("result.txt",'r')

Total = ''
Vector = []

for line in json_data:
	for letter in line:
		Total+=letter
		if letter == "}":
			Vector.append(Total)
			Total = ''

Users = []

for v in Vector:
	try:
		Test = json.loads(v)
		if Test["user_id"] not in Users:
			Users.append(Test["user_id"])
	except:
		continue

#Users = Users[::-1]
    
# find who a specific user follows. Change the screen name below
Friends = {}

for user in Users:
	home_timeline = oauth_req( 'https://api.twitter.com/1.1/friends/ids.json?user_id=' +str(user), '80996230-1AQmU1rFemflCOW3B2I6w8OTxGDv0Qq97zI6fZVpZ', 'WY7T0QjGE5q98KDDsIiPnpjQuTXCmGkzanzYSUYMt8Ng6' )
	if home_timeline !=[]:
		ids = json.loads(home_timeline)["ids"]
		Friends = {}
		Friends[user] = [ids]
		"""
		try:
			Friends[user].append(ids)
		except KeyError:
			Friends[user] = [ids]
		"""
		json.dump(Friends, w)
		