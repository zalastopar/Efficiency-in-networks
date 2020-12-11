from graphs import *
import pandas
from functools import reduce
from operator import mul

# Sim povprečje za vse (velike) grafe
columns = ["Percent", "Avg. efficiency", "Sim 10", "Sim 100", "Sim 1000"]
columns_removed = ["Percent", "Random", "Centered"]
data = {}                   # Za sim

PERCENTS = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]
GRID_DIMS = [1, 2, 3, 4, 5, 10, 20, 50, 100]
TREE_DEPTHS = range(2, 21)
CYCLE_LENGTHS = [2, 3, 4, 5, 10, 20, 50, 100, 200, 300, 400, 500, 1000, 10000, 100000, 1000000]

class GraphGenerator:
    def __init__(self, *params):
        self.params = params

    def __str__(self):
        return self.STR.format(*self.params)

    def format(self, percent):
        return self.FORMAT.format(*self.params, percent)

    def generate(self):
        return self.__class__.GENERATE(*self.params)

class Grid3D(GraphGenerator):
    GENERATE = generate_3d_grid
    STR = 'grid {}x{}x{}'
    FORMAT = 'Grid {}x{}x{} at {}'

    def __len__(self):
        return reduce(mul, self.params)

class Tree(GraphGenerator):
    GENERATE = generate_binary
    STR = 'tree size {}'
    FORMAT = 'Tree {} at {}'

    def __len__(self):
        return int(pow(2, *self.params)) - 1

class Cycle(GraphGenerator):
    GENERATE = generate_cycle
    STR = 'cycle size {}'
    FORMAT = 'Cycle {} at {}'

    def __len__(self):
        return self.params[0]

graphs = sorted([Grid3D(i, j, k) for ii, i in enumerate(GRID_DIMS[1:], 1)
                                 for jj, j in enumerate(GRID_DIMS[:ii+1])
                                 for k in GRID_DIMS[:jj+1]] +
                [Tree(i) for i in TREE_DEPTHS] + [Cycle(i) for i in CYCLE_LENGTHS],
                key=len)

for G in graphs:
    graph = G.generate()
    for percent in PERCENTS:
        print('working on {}'.format(G))                     # Spremeni stevilke
        graph_data = []
        for _ in range(1000):
            graph_data.append(average_sim(graph, percent))
        data[G.format(percent)] = [percent, average_efficiency(graph),
                                   sum(graph_data[:10])/10, sum(graph_data[:100])/100,
                                   sum(graph_data)/1000]
        df = pandas.DataFrame.from_dict(data, orient='index')
        df.columns = columns
        df.to_csv('Data/Sim.csv')
