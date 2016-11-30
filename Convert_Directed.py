import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigs
from statistics import median

#Simple Example txt file with entries of an adjacency matrix, weights
f = open('adjacency.txt')

#Initialize
Row     = []
Col     = []
W_in    = []
W_out   = []
Weights = []

#Creates weighting matrix
def set_list(W,i,w):
	try:
		W[i] = w
	except IndexError:
		for _ in range(0,i-len(W)+1):
			W.append(0)
		W[i] += w
	return W

#Create scipy sparse adjacency matrix and weighting matrix
for line in f:     
	line = (line.split())
	
	r = int(line[0])
	c = int(line[1])
	w = float(line[2])
	
	Row.append(r)
	Col.append(c)
	Weights.append(w)
	
	W_in  = set_list(W_in,c,w)
	W_out = set_list(W_out,r,w)

Lr = len(W_out)
Lc = len(W_in)

#Make sure in and out weighting matrices are same length
if Lr<Lc :
	for i in range(0,Lc-Lr):
		W_out.append(0)
if Lr > Lc:
	for i in range(0,Lr-Lc):
		W_in.append(0)	

#Computations for degree discounted weighting matrix		
alpha = 0.5
for i in range(0,len(W_in)):
	if W_in[i]>0:
		W_in[i] = 1/(W_in[i]**alpha)
	if W_out[i]>0:
		W_out[i] = 1/(W_out[i]**alpha)


L = max(Row+Col)+1
Ind = range(0,L)

#Use sparse library to create matrices
A   = coo_matrix((Weights,(Row,Col)),shape =(L,L))

D_in = coo_matrix((W_in,(Ind,Ind)),shape =(L,L))
D_out = coo_matrix((W_out,(Ind,Ind)),shape =(L,L))

B = D_out*A*D_in*np.transpose(A)*D_out
C = D_in*np.transpose(A)*D_out*A*D_in

#Symmeterization
As  = A+np.transpose(A)

#Bibliometric
Ab  = A*np.transpose(A)+np.transpose(A)*A

#Degree_Discounted
Au = B+C









