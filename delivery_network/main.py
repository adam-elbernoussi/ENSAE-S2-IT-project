from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.1.in"

g = graph_from_file(data_path + file_name)
print(g)

import time
#We will reach the time needed to find the min power of the first ten traject of routes.1.in
with open("/home/onyxia/work/ENSAE-S2-IT-project/input/routes.1.in", "r") as file:
    t1 = time.perf_counter()
    for _ in range(10):
        _tmp = list(map(int, file.readline().split()))
        if len(_tmp) == 3:
            node1, node2, _= _tmp
            g.min_power(node1, node2)
    t2= time.perf_counter()
#print(t2-t1) output : 0.0013727350160479546
#hence the time needed to calculate min power of each traject of the file routes.1.in is 0.0013727350160479546*14 = 0.01921829022


def kruskal(graph) :
    #tri des arêtes par ordre croissant de poids
    edges=sorted(graph.edges,key=lambda x:x[2])
    #Initialisation de la strucuture Union-Find
    parent=list(range(graph.n))
    
    def find(x):
        if parent[x]==x:
            return x
        parent[x]=find(parent[x])
        return parent[x]
    
    def union(x,y):
        parent[find(x)]=find(y)
    
    #construction de l'arbre couvrant de poids minimal
    mst=Graph(graph.n)
    for u,v,w in edges:
        if find(u)!=find(v):
            mst.add_edge(u,v,w)
            union(u,v)
    return mst
