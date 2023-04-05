from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.2.in"

g = graph_from_file(data_path + file_name)
#print(g)
#g.view()


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

    res = dict([[i, 0] for i in range(1, 3)]) # type: ignore #warning we should put range(1, 11) here
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
    return dict([["routes.{}.in".format(i), res[i]] for i in range(1, 3)]) #warning we should put range(1, 11) here
    #this function seems to be ok for network 1 or 2

"""
On va répondre à la question 10 à l'aide de ce commentaire
Soit un graphe G et A un arbre couvrant de poids minimal du graphe G. On considère T un trajet de G. 

Déjà,il est clair que 
Puissance minimale pour couvrir T dans G <= Puissance minimale pour couvrir T dans A

De plus, distinguons deux cas : 

Cas 1 : Il existe une arrête de T qui n'est pas dans A. 
On appelle C le sous graphe de G formé de l'ensemble des arêtes de T qui sont dans A, et de l'ensemble des 
arêtes de T qui ne sont pas dans A.
Soit B un arbre couvrant de poids minimal du graphe C
Alors B couvre tous les sommets de T (Car B contient toutes les arrêtes de T). Notons D le sous graphe de G composé de 
l'ensemble des arrêtes de T qui sont dans A. Puisque A est un arbre couvrant de poids minimal pour G, il est aussi un 
arbre couvrant de poids minimal pour D. Donc somme des poids des arrêtes dans A <= somme des poids des arrêtes dans B.

De plus, B contenant toutes les arrêtes de T qui sont dans A, 
Puissance minimale pour couvrir T dans A <= Puissance minimale pour couvrir T dans B
Par le théorème de sous-optimalité de l'arbre de poids minimal, 
Puissance minimale pour couvrir T dans A = Puissance minimale pour couvrir T dans B
Or il est clair que la puissance minimale pour couvrir T dans B est égale à la puissance minimale pour couvrir T dans G
D'où Puissance minimale pour couvrir T dans A = Puissance minimale pour couvrir T dans G 

D'où le résultat

Cas 2 : T se trouve totalement dans A. Alors toutes les arrêtes de T qui sont dans A ont un poids nul
et sont donc nécessaire pour couvrir T. Le résultat est alors clair.

"""

from graph import kruskal, min_power_for_path
#We will now create files routes.xx.out
for i in range(2, 3):
    g = graph_from_file("input/network.{}.in".format(i))
    g = kruskal(g)
    route = open("input/routes.{}.in".format(i), "r")
    fichier = open("routes.{}.out".format(i), "w")
    n = int(list(map(int, route.readline().split()))[0]) # not opti
    for i in range(n):
        print(i)
        source, destination, _ = map(int, route.readline().split())    
        fichier.write("{}\n".format(min_power_for_path(g, source, destination)))
