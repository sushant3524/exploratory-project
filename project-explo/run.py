import dataset
import functions
G=dataset.G
x=dataset.x
label=dataset.label
TP=dataset.TP
n=dataset.n
A=[0 for i in range(n)]
k=dataset.k
t=0
functions.inpro(G,x,A,label,TP,t,k)
c=0
for i in range(len(A)):
	if(A[i]==1):
		c+=1
print("Count of recommendations accepted: ",c)
print("Final attitude status of all the nodes: ")
print(A)
print("Total number of edges in the graph: ",G.number_of_edges())
print("The number of nodes recommending an add to a node is roughly: ",G.number_of_edges()//n)