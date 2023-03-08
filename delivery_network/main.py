from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)

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
