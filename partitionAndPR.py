import networkx
from networkx import number_of_nodes
import operator
import community

f = open('user_retweet_list.txt','r')
G = networkx.Graph()
for line in f:
	splits = line.split()
	G.add_edge(splits[0], splits[1])
partition = community.best_partition(G)
n = partition[max(partition.items(), key=operator.itemgetter(1))[0]]
print(n)
for i in range(int(n)):
	print("Doing group ", i)
	G = networkx.Graph()
	f.seek(0)
	for line in f:
		splits = line.split()
		if partition[splits[0]] != i:
			continue
		if partition[splits[1]] != i:
			continue
		G.add_edge(splits[0], splits[1])
	if number_of_nodes(G) > 100:
		pr = networkx.pagerank(G)
		print(sorted(pr.items(), key=operator.itemgetter(1), reverse=True)[:1])