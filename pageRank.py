import networkx
import operator
f = open('user_retweet_list.txt','r')
G = networkx.Graph()
for line in f:
	splits = line.split()
	G.add_edge(splits[0], splits[1])
pr = networkx.pagerank(G)
print pr
print sorted(pr.items(), key=operator.itemgetter(1), reverse=True)[:10]