import json
edge_list = open('user_retweet_list.txt', 'w')
all_user_id = {}
def find_user_data(filename):
	global all_user_id
	f = open(filename,'r')
	data = f.read()
	splits = data.split('}{')
	splits[0] = splits[0][1:]
	# For some reason the last one isn't built correctly, need to append ]]
	splits[-1] = splits[-1][:-1] +']]'
	user_friends_map = {}
	for js in splits:
		jss = '{' + js + '}'
		user_friends_map = json.loads(jss)
		for user, val in user_friends_map.iteritems():
			all_user_id[int(user)] = True
	f.close()

def add_file_data(filename):
	global edge_list
	global all_user_id
	f = open(filename,'r')
	data = f.read()
	splits = data.split('}{')
	splits[0] = splits[0][1:]
	# For some reason the last one isn't built correctly, need to append ]]
	splits[-1] = splits[-1][:-1] +']]'
	count = 0
	user_friends_map = {}
	for js in splits:
		jss = '{' + js + '}'
		try:
			tweet_map = json.loads(jss)
			user = tweet_map["user_id"]
			if "retweeted_author_id" in tweet_map:
				retweeted_author = tweet_map["retweeted_author_id"]	
				if retweeted_author not in all_user_id:
					continue
				edge_list.write(str(user)+' '+str(retweeted_author)+'\n')
				count += 1
		except:
			pass
	f.close()
	print "total edges: ", count

find_user_data('result1.csv')
find_user_data('result2.csv')
add_file_data('resultBackup.txt')
edge_list.close()
