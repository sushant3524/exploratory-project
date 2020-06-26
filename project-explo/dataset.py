import random
import networkx as nx
# Synthetic Graph Data Generation
random.seed(10)
n=100
G=nx.gnp_random_graph(n,0.1,seed=10,directed=True)
label={}
c=0;
for (u,v) in G.edges():
	G.edges[u,v]['weight']=random.uniform(0,1)
	if(c%2):
		label[u,v]=1
	else:
		label[u,v]=-1
	c+=1
		
x=[]
TP=[]
for i in range(n):
	x.append(random.uniform(0,1))
	TP.append([random.randrange(0,50)])
	TP[i].append(TP[i][0]+random.randrange(0,10))
t=0
k=5