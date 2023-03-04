# À compléter
import sys 
sys.path.append("delivery_network")

from Mathieu import Graph, graph_from_file

import unittest   # The test framework
class Test_GraphLoading2(unittest.TestCase):
    def test_network4_1(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.nb_nodes, 10) #pas très utile car déja vérifié en q1
        self.assertEqual(g.nb_edges, 4) #pas très utile car déja vérifié en q1
        self.assertEqual(g.graph[2][1][2], 89) #la distance de l'arete qui relie 1 à 2 est 89

    def test_network4_2(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.graph[1][0][2], 6) #la distance de l'arete qui relie 1 à 4 est 89

if __name__ == '__main__':
    unittest.main()