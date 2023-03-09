from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.1.in"

g = graph_from_file(data_path + file_name)
print(g)
#g.view()

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

    res = dict([[i, 0] for i in range(1, 3)]) #warning we should put range(1, 11) here
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

print(time_array())