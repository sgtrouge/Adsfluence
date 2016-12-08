import json
import pandas as pd
import csv
import pylab as p
import seaborn
import numpy as np
import matplotlib.pyplot as plt
w = open("tweet_info.csv", "w")

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
columns = ["content","user_id","retweeted_author_id","timestamp"]
keywords = ['GoBlue', 'Ann Arbor', 'UMich', 'Michigan Wolverines', 'BigHouse', 'University of Michigan', 'Duderstadt', 'Yost arena', 'Crisler Center']
Data = pd.DataFrame()

Followers = []
Following = []
Retweets  = {}
Tweets    = {}


for v in Vector:
	try:
		Json = json.loads(v)
		if Json['retweeted_author_id']!=[]:
			RT = Json['retweeted_author_id']
			Retweets[RT] = Retweets.get(RT,0)+1
		if Json["user_id"] not in Users:		
			Users.append(Json["user_id"])
			Followers.append(Json['user_follower_count']+1)			
		ID  = Json['user_id']
		Tweets[ID]=Tweets.get(ID, 0) + 1
		
	except:
		continue


Number_tweets = Tweets.values()
Number_RT     = Retweets.values()
		

#Plot the data

print np.mean(Followers)
print np.max(Followers)
print np.min(Followers)


"""
plt.hist(np.log2(Followers),bins=50,log=True)
plt.xlabel("Number of Followers (Log Scale)")
plt.ylabel("Frequency (Log Scale)")
plt.show()

plt.hist(np.log2(Number_RT),bins=50,log=True)
plt.xlabel("Number of Retweets (Log Scale)")
plt.ylabel("Frequency (Log Scale)")
plt.show()

plt.hist(np.log2(Number_tweets),bins=50,log=True)
plt.xlabel("Number of Tweets (Log Scale)")
plt.ylabel("Frequency (Log Scale)")
plt.show()
"""