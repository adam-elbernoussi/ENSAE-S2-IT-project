class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    

    def get_path_with_power(self, src, dest, power):
        visited = set()
        stack = [(src, [], 0)]  # (node, path, total power)
        while stack:
            node, path, total_power = stack.pop()
            if node == dest and total_power <=power:
                return path + [dest]
            if node not in visited:
                visited.add(node)
                for neighbor, min_power, _ in self.graph[node]:
                    if min_power <= power and neighbor not in visited:
                        stack.append((neighbor, path + [node], max(min_power, total_power)))
        return None
    
    #complexit?? en O(V+E)


    def connected_components(self):
        visited = set()
        components = []
        for node in self.nodes:
            if node not in visited:
                component = []
                self._dfs(node, visited, component)
                components.append(component)
        return components

    def _dfs(self, node, visited, component):
        """
        Depth-first search implementation used by the connected_components method.
        As indicated in the guideline
        """
        visited.add(node)
        component.append(node)
        for neighbor, _, _ in self.graph[node]:
            if neighbor not in visited:
                self._dfs(neighbor, visited, component)


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        #Using binary research
        #This part is for security : avoid the case where hte while loop goes infinite
        src_dest_same_connected_component = False
        for a in self.connected_components_set():
            if {src, dest} < a:
                src_dest_same_connected_component = True
        #Find min and max of edges' weight 
        _tmp = []
        for i in self.graph:
            for j in self.graph[i]:
                _tmp.append(j[1])
        a = min(_tmp)
        b = max(_tmp)
        #From this point it is the real function
        if src_dest_same_connected_component:
            while (b-a) >= 1:
                if self.get_path_with_power(src, dest, (a+b)/2) != None:
                    b = (a+b)/2
                else : 
                    a = (a+b)/2
            return self.get_path_with_power(src, dest, int(b)), int(b)     #assumed here that power is always an integer 
        raise ValueError("The two given nodes are not in the same connected component.")
    
    def view(self, node1 = None, node2 = None):
        """
        This function allow a visualisation of a graph

        Actually this function takes 2 nodes of the graph and display the entire graph with
        the shortest path between the two nodes in red
        If the function does not recieve two nodes it will simply display the graph
        The function automatically save the Graph in the file ../graph_viz_output

        Parameters:
        -----------
        node1 : NodeType
            A node of the graph
        node2 : NodeType
            Another node of the graph
        
        Outputs:
        -----------
        None
        """
        import graphviz
        dot = graphviz.Graph('Graph', comment='Graph visualisation', graph_attr = {"concentrate" : 'True'})
        verified_edge = []
        for i in self.graph:
            dot.node('{}'.format(i))
        if ((node1 != None) and (node2 != None)):
            path, _ = self.min_power(node1, node2)
            for i in self.graph:
                if i in path:
                    dot.node('{}'.format(i), color = 'red', fontcolor = 'red')
                for j in self.graph[i]: #we can probably optimize/clarify this double for loop
                    if ({i, j[0]} not in verified_edge) and (i in path) and (j[0] in path):
                        if (i == path[0]) and (j[0]== path[-1]) and (len(path) != 2):
                            dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                            #Actually the method Graphviz.edge automatically create the node
                            verified_edge.append({i, j[0]})
                        else:
                            dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]), color = 'red')
                            #Actually the method Graphviz.edge automatically create the node
                            verified_edge.append({i, j[0]})
                    elif {i, j[0]} not in verified_edge:
                        dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                        verified_edge.append({i, j[0]})
            dot.render(directory='graph_viz_output', view=True)
        else: 
            for i in self.graph:
                for j in self.graph[i]: #we can probably optimize/clarify this double for loop
                    if {i, j[0]} not in verified_edge:
                        dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                        verified_edge.append({i, j[0]})
            dot.render(directory='graph_viz_output', view=True)



def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters:
    -----------
    filename: str
        The name of the file

    Outputs:
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g


def kruskal(g):
    #tri des ar??tes par ordre croissant de poids
    set_edges = []
    for a in g.graph:
        for j in g.graph[a]:
            set_edges.append([a, j[0], j[1]])
    edges=sorted(set_edges,key=lambda x:x[2])
    #Initialisation de la strucuture Union-Find
    parent = list(g.nodes)
    #parent = [x-1 for x in list(g.nodes)]
    print(parent)
    
    def find(x):
        #print(x)
        if parent[x-1]==x:
            return x
        parent[x-1]=find(parent[x-1])
        return parent[x-1]
    
   #def find_2(x):
        #print(x)
        #if parent[x-1]==x:
        #    return x
        #parent[x-1]=find(parent[x-1])
        #return parent[x-1]

    def union(x,y):
        parent[find(x)-1]=find(y)
    
    #construction de l'arbre couvrant de poids minimal
    g_mst=Graph(list(g.nodes))
    for u,v,w in edges:
        if find(u)!=find(v):
            g_mst.add_edge(u,v,w)
            union(u,v)
    return g_mst


def min_power_for_path(g, t):
    # Calcul de l'arbre couvrant de poids minimal
    mst = kruskal(g)

    # Recherche du chemin entre les deux extr??mit??s du trajet t dans l'arbre couvrant
    start, end = t[0], t[-1]
    path = [start]
    curr = start
    while curr != end:
        neighbors = mst.graph[curr]
        for neighbor, weight in neighbors:
            if neighbor not in path:
                path.append(neighbor)
                curr = neighbor
                break

    # Calcul de la puissance minimale requise pour couvrir le trajet
    power = 0
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        edge_weight = g.get_edge_weight(u, v)
        power = max(power, edge_weight)

    return power, path

####################################################################################################################################################################################
#                   test
####################################################################################################################################################################################

#g = graph_from_file("input/network.05.in")
#print(g)
#print(g.min_power(1, 2), g.connected_components_set())
#g.view()
#kruskal(g).view()
route = open("input/routes.1.in", "r")
n = list(map(int, route.readline().split()))[0]
print(n)
