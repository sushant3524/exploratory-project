import numpy as np
from sklearn.preprocessing import normalize
#Taking the number of nodes to be 100, will generate a graph wwith same number of nodes
import dataset
n=dataset.n

def inpro(G,x,A,label,TP,t,k):
	if t==0:
		S=SPR(G,x,label,k)
		for i in range(len(S)):
			A[S[i]]=1
	else:
		S=set()
		for i in range(len(A)):
			if(A[i]==1):
				S.add(i)
	fa=[]
	fb=[]
	for i in range(n):
		if i not in S and t>=TP[i][0] and t<=TP[i][1]:
			fa.append(i)
		elif i not in S and t<TP[i][0]:
			fb.append(i)
	if len(fa)==0 and len(fb)!=0:
		t=t+1
		inpro(G,x,A,label,TP,t,k)
	elif len(fa)!=0:
		t=t+1
		(x,A)=BUpdate(G,x,A,label,S)
		for i in range(n):
			if i not in S and A[i]==1:
				if 1-x[i]>=0.7:#let the threshold on revoking the advertisement after accepting be 0.7
					A[i]=0
		inpro(G,x,A,label,TP,t,k)
	else:
		print("The total time taken for propogation: ",t)


def BUpdate(G,x,A,label,S):
	pos=0.0
	neg=0.0

	for v in range(n):
		alp=0.0
		bet=0.0
		pos=0.0
		neg=0.0
		if A[v]==1:
			continue
		for u in S:
			if v in G.neighbors(u):
				if label[u,v]==1:
					pos=pos+G.edges[u,v]['weight']*(x[u]-x[v])
					alp=alp+1
				else:
					neg=neg+G.edges[u,v]['weight']*(x[u]-x[v])
					bet=bet+1
		if(alp):
			x[v]=x[v]+pos*(alp/(alp+bet))
		if(bet):
			x[v]=x[v]-neg*(bet/(alp+bet))
		#let threshold limit of belief for attitude to be 1 be 0.7
		if x[v]>=0.7:		
			A[v]=1
	return x,A		

def SPR(G,x,label,k=5):
	t=0
	W=np.zeros((n,n))
	L=np.zeros((n,n))
	#taking value of damping coefficient to be 0.85
	d=0.85
	for (u,v) in G.edges():
	    W[u][v]=G.edges[u,v]['weight']
	    L[u][v]=label[u,v]
	W=normalize(W,axis=1,norm='l1')
	Y=np.multiply(W,L)
	Y*=d

	curr_SPR=x
	next_SPR=[0 for i in range(0,n)]
	curr_sort=[i for i in range(1,n+1,1)]
	temp=sorted(curr_SPR,reverse=True)
	next_sort=[(temp.index(curr_SPR[i]))+1 for i in range(n)]

	while next_sort!=curr_sort:
	    for i in range(n):
	        curr_sort[i]=next_sort[i]
	    for i in range(n):
	        for j in G.neighbors(i):
	            next_SPR[i]+=(curr_SPR[i]-curr_SPR[j])*Y[i][j]+(1-d)/n
	    temp=sorted(next_SPR,reverse=True)
	    for i in range(n):
	        next_sort[i]=temp.index(next_SPR[i])+1
	    for i in range(n):
	        curr_SPR[i]=next_SPR[i]
	        next_SPR[i]=0
	    t+=1

	S=[]
	for i in range(n,n-k,-1):
		S.append(curr_sort.index(i))
	return S