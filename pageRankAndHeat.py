import networkx
import operator
import sys
import math

import collections
import time
import random
f = open('user_follow_list.txt','r')
G = networkx.DiGraph()
for line in f:
	splits = line.split()
	G.add_edge(splits[0], splits[1])
pr = networkx.pagerank(G)
#print pr
#print sorted(pr.items(), key=operator.itemgetter(1), reverse=True)[:10]


def compute_psis(N,t):
    psis = {}
    psis[N] = 1.
    for i in xrange(N-1,0,-1):
        psis[i] = psis[i+1]*t/(float(i+1.))+1.
    return psis

Gvol = G.number_of_edges()
## Setup parameters that can be computed automatically
N = 47 # see paper for how to set this automatically
t = 15.
eps = 0.0001
psis = compute_psis(N,t)
x = {}
r = {}

currun = 0
    
while 1:
    if currun%15==0:
        # print out the header
        print
        print
        print "%10s  %5s  %4s  %4s  %7s  %7s  %7s"%(
                'seed ID','degree','time','cond','edges','nnz','setsize')
    currun += 1
        
    time.sleep(0.5)
    randiseed = random.randint(1, len(G))
    seed = ['270989555']
    start = time.time()

    ## Estimate hkpr vector 
    # 
    # This is our main algorithm.
    # 
    # G is a networkx graph, or something that implements the same
    # interface
    #
    # t, tol, N, psis are precomputed
    # npush tracks number of operations
    x = {} # Store x, r as dictionaries
    r = {} # initialize residual
    Q = collections.deque() # initialize queue
    npush = 0.

    for s in seed: 
        r[(s,0)] = 1./len(seed)
        Q.append((s,0))
    npush += len(seed)
    while len(Q) > 0:
        (v,j) = Q.popleft() # v has r[(v,j)] ...
        rvj = r[(v,j)]
        # perform the hk-relax step
        if v not in x: x[v] = 0.
        x[v] += rvj 
        r[(v,j)] = 0.
        update = rvj/G.out_degree(v)
        mass = (t/(float(j)+1.))*update
        for u in G[v]:   # for neighbors of v
            next = (u,j+1) # in the next block
            if j+1 == N: 
                x[u] += update
                continue
            if next not in r: r[next] = 0.
            thresh = math.exp(t)*eps*G.out_degree(u)
            thresh = thresh/(N*psis[j+1])
            if r[next] < thresh and \
                r[next] + mass >= thresh:
                Q.append(next) # add u to queue
            r[next] = r[next] + mass
        npush += G.out_degree(v)

    ## Step 2 do a sweep cut based on this vector 
    # Find cluster, first normalize by degree
    for v in x: x[v] = x[v]/G.out_degree(v)
  
    # now sort x's keys by value, decreasing
    sv = sorted(x.iteritems(), key=lambda x: x[1], reverse=True)
    S = set()
    volS = 0.
    cutS = 0.
    bestcond = 1.
    bestset = sv[0]
    for p in sv:
      s = p[0] # get the vertex
      volS += G.out_degree(s) # add degree to volume
      for v in G[s]:
        if v in S:
          cutS -= 1
        else:
          cutS += 1
      S.add(s)
      if cutS/min(volS,Gvol-volS) < bestcond:
        bestcond = cutS/min(volS,Gvol-volS)
        bestset = set(S) # make a copy
    
    # print out the info on this cluster
    print "%s  %5i  %4.2f  %4.2f  %7i  %7i  %7i"%(
        seed[0], G.out_degree(seed[0]),
        time.time()-start, bestcond,
        npush, len(x), len(bestset))