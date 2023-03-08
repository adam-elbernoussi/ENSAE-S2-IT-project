from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.1.in"

g = graph_from_file(data_path + file_name)
print(g)

import time #import the module time
def time_array():
    """
    This function takes no parameters and simply return a DataFrame with the average time needed
    to calculate all the power min of a routes.xx.in file
    
    Parameters:
    -----------
        None

    Outputs:
    -----------
    df : Pandas.DataFrame
        A Dataframe of one row with the average time needed to calculate all the power min of a routes.xx.in file
    """
    import time #import the module time

    res = dict([[i, 0] for i in range(1, 2)])
    for i in res:
        g = graph_from_file("input/network.{}.in".format(i))
        with open("input/routes.{}.in".format(i), "r") as file:
            n = int(file.readline().split()[0])
            t1 = time.perf_counter()
            for _ in range(10):
                _tmp = list(map(int, file.readline().split()))
                node1, node2, _= _tmp
                g.min_power(node1, node2)
            t2 = time.perf_counter()
        res[i] = ((t2-t1)/10)*n
    return dict([["routes.{}.in".format(i), res[i]] for i in range(1, 2)]) 



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

print(time_array())