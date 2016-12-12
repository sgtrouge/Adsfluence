import oauth2
import time
import json
from pprint import pprint
import pandas as pd
from django.utils.encoding import smart_str
import pickle
import csv
w = open(".data/tweet_info.csv", "w")

json_data = open("thanksgiving.txt",'r')

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
keywords = ['GoBlue', 'Ann Arbor', 'UMich', 'Wolverines', 'BigHouse', 'University', 'Duderstadt', 'Yost arena', 'Crisler','none']

Data = pd.DataFrame()

User_id = []
Content=[]
Retweet_id = []
Time  =[]
Keyword = []

for v in Vector:
	try:
		Json = json.loads(v)
		if Json['retweeted_author_id']==[]:
			continue
		Text = Json['content']
		for k in range(0,len(keywords)):
			if keywords[k] in Text:
				break
		User_id.append(Json['user_id'])
		Content.append(Json['content'])
		Retweet_id.append(Json['retweeted_author_id'])
		Time.append(Json['timestamp'])
		Keyword.append(k)
	except:
		continue

Data['content'] = Content	
Data['user_id'] = User_id	
Data['retweet_id'] = Retweet_id	
Data['time'] = Time
Data['keyword'] = Keyword

#Output to csv file
Data.to_csv('Tweet_Info_TGiving.csv',sep=',',index=False,encoding='utf-8')

