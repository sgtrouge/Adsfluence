import json
edge_list = open('user_follow_list.txt', 'w')

all_user_id = {}
from_graph_user_id = {}
count = 0
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
	global count
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
			val_only = val[0]
			for friend in val_only:
				if friend not in all_user_id:
					continue
				edge_list.write(str(user)+' '+str(friend)+'\n')
				count += 1
	f.close()
find_user_data('result1.csv')
find_user_data('result2.csv')
# print all_user_id
add_file_data('result1.csv')
add_file_data('result2.csv')
print "number of nodes", len(list(all_user_id.keys()))
print "number of edges", count
edge_list.close()
