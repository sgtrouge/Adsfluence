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
