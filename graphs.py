from graph import Graph, Graph3D
import graph
from graph.visuals import plot_3d, plot_2d
import math
import random
import pandas

graf = Graph()
graf.add_node("a")
graf.add_node("b")
graf.add_edge("a", "b")
graf.add_node("c")
graf.add_edge("a", "c")


# Generating a 1xn grid
    
def generate_1xn(n):
    grid_1xn = Graph()
    for i in range(1, n + 1):
        grid_1xn.add_node(i)
        if i > 1:
            grid_1xn.add_edge(i, i-1, 1)
            grid_1xn.add_edge(i-1, i, 1)
    return grid_1xn


# Generating a mxn grid:
# (We could easily generate a 1xn grid using the following code as well)

def generate_mxn(m, n):
    grid_mxn = Graph()
    for i in range(1, n+1):
        for j in range(1, m+1):
            grid_mxn.add_node(str(i) + ',' + str(j))
            if i > 1:
                grid_mxn.add_edge(str(i) + ',' + str(j), str(i-1) + ',' + str(j), 1)
                grid_mxn.add_edge(str(i-1) + ',' + str(j), str(i) + ',' + str(j), 1)
            if j > 1:
                grid_mxn.add_edge(str(i) + ',' + str(j), str(i) + ',' + str(j-1), 1)
                grid_mxn.add_edge(str(i) + ',' + str(j-1), str(i) + ',' + str(j), 1)
    return grid_mxn


# Generating a perfect binary tree with deisred height:

def generate_binary(height):
    graph_binary = Graph()
    for i in range(1, height + 1):
        for j in range(1, int(2**(i-1) + 1)):
            graph_binary.add_node(str(i) + ',' + str(j))
            if i > 1:
                graph_binary.add_edge(str(i-1) + ',' + str(math.ceil(j/2)), str(i) + ',' + str(j), 1)
                graph_binary.add_edge(str(i) + ',' + str(j), str(i-1) + ',' + str(math.ceil(j/2)), 1)
    return graph_binary


# Generating a cycle with n nodes:
# We are going to use the generate_1xn function and add 2 edges

def generate_cycle(n):
    graph = generate_1xn(n)
    if n > 1:
        graph.add_edge(1, n, 1)
        graph.add_edge(n, 1, 1)
    return graph


# Generating a 3D grid (m x n x p):

def generate_3d_grid(m, n, p):
    grid = Graph()
    for i in range(1, n+1):
        for j in range(1, m+1):
            for k in range(1, p+1):
                grid.add_node(str(i) + ',' + str(j) + ',' + str(k))
                if i > 1:
                    grid.add_edge(str(i) + ',' + str(j) + ',' + str(k), str(i-1) + ',' + str(j) + ',' + str(k), 1)
                    grid.add_edge(str(i-1) + ',' + str(j) + ',' + str(k), str(i) + ',' + str(j) + ',' + str(k), 1)
                if j > 1:
                    grid.add_edge(str(i) + ',' + str(j) + ',' + str(k), str(i) + ',' + str(j-1) + ',' + str(k), 1)
                    grid.add_edge(str(i) + ',' + str(j-1) + ',' + str(k), str(i) + ',' + str(j) + ',' + str(k), 1)
                if k > 1:
                    grid.add_edge(str(i) + ',' + str(j) + ',' + str(k), str(i) + ',' + str(j) + ',' + str(k-1), 1)
                    grid.add_edge(str(i) + ',' + str(j) + ',' + str(k-1), str(i) + ',' + str(j) + ',' + str(k), 1)
    return grid


# Generating an ideal graph with n nodes:

def generate_ideal(n):
    ideal = Graph()
    for i in range(1, n + 1):
        ideal.add_node(i)
    for start in ideal.nodes():
        for end in ideal.nodes():
            if start != end:
                ideal.add_edge(start, end, 1)
                ideal.add_edge(end, start, 1)
    return ideal


# Generating random graph on n nodes:

def generate_random(n):
    number_of_edges = random.randrange(2, n*(n-1)) 
    rand = generate_1xn(n)
    for i in range(1, n):
        rand.add_node(i)
    while len(rand.edges()) < number_of_edges:
        first = random.choice(rand.nodes())
        node = [nod for nod in rand.nodes() if nod != first]
        second = random.choice(node)
        if rand.edge(first, second) == None:
            rand.add_edge(first, second, 1)
    return rand


# The following functions calculate various efficiencies of a graph
# We used some of pre-written functions from graph-theory library


def average_efficiency(graph):
    total = 0
    for start in graph.nodes():
        partial = 0
        for end in graph.nodes():
            if start != end:
                partial += 1/graph.shortest_path(start, end)[0]
        total += partial
    if len(graph.nodes())<= 1:
        return 0
    return total / (len(graph.nodes()) * (len(graph.nodes())-1))


def global_efficiency(graph, ideal):
    try:
        return average_efficiency(graph)/average_efficiency(ideal)
    except ZeroDivisionError:
        return 0

def local_efficiency(graph):
    total = 0
    for node in graph.nodes():
        podgraf = graph.subgraph_from_nodes(graph.network_size(node, 1))
        podgraf.del_node(node)
        total += average_efficiency(podgraf)
    return total / len(graph.nodes())



# So far so good! :)

# The following functions calculate efficiencies by only considering a random subset of pairs rather than all possible pairs of vetrices.
# Functions are given an argument that tells them what percentage of pairs to select
# If the percent given is over 50%, then takes a different approach
def average_sim(graph, percent):
    pairs = set()
    all_pairs = set()
    for first in graph.nodes():
        for second in graph.nodes():
            if first != second:
                all_pairs.add((first, second))
    lay = False
    if percent > 0.5:
        percent = 1 - percent
        lay = True
    while len(pairs) < min(len(graph.nodes())* (len(graph.nodes()) - 1) * percent, len(graph.nodes())* (len(graph.nodes()) - 1) * (1 - percent)):
        first = random.choice(graph.nodes())
        second = random.choice(graph.nodes())
        if first != second:
            pairs.add((first, second))
    if lay:
        pairs = all_pairs - pairs
    total = 0
    for pair in pairs:
        total += 1 / graph.shortest_path(pair[0], pair[1])[0]
    return total / len(pairs)

def global_sim(graph, percent):
    pairs = set()
    all_pairs = set()
    for first in graph.nodes():
        for second in graph.nodes():
            if first != second:
                all_pairs.add((first, second))
    lay = False
    if percent > 0.5:
        percent = 1 - percent
        lay = True
    while len(pairs) < min(len(graph.nodes())* (len(graph.nodes()) - 1) * percent, len(graph.nodes())* (len(graph.nodes()) - 1) * (1 - percent)):
        first = random.choice(graph.nodes())
        second = random.choice(graph.nodes())
        if first != second:
            pairs.add((first, second))
    if lay:
        pairs = all_pairs - pairs
    # Might change also:
    return average_sim(graph, percent)/average_sim(generate_ideal(len(graph.nodes())))

def local_sim(graph, percent):
    pass


# Function to remove a percentage of edges (chosen randomly)
def remove_random(graph, percent):
    resitev = graph
    lay = False
    if percent > 0.5:
        lay = True
        percent = 1 - percent
    edges = graph.edges()
    chosen = set()
    while len(chosen) < percent * len(edges):
        edge = random.choice(edges)
        if edge not in chosen:
            chosen.add(edge)
            chosen.add((edge[1], edge[0], edge[2]))
    if lay:
        zacasno = edges
        for el in chosen:
            zacasno.remove(el)
        chosen = zacasno
    for (first, second, _) in chosen:
        try:
            resitev.del_edge(first, second)
            resitev.del_edge(second, first)
        except:
            pass
    return resitev

# Function to remove a percentage of edges (centered around a randomly selected node and its neighbor nodes)
def remove_centered(graph, percent, start = None):
    resitev = graph
    total_edges = len(graph.edges())
    if start == None:
        start = random.choice(graph.nodes())
    queue = [start]
    done = []
    while len(resitev.edges()) > (1 - percent) * total_edges and queue != []:
        node = queue[0]
        queue.remove(node)
        for el in graph.nodes(from_node = node):
            if len(resitev.edges()) <= (1 - percent) * total_edges:
                break
            if el not in done:
                queue.append(el)
            try:
                resitev.del_edge(node, el)
                resitev.del_edge(el, node)
            except:
                continue
        done.append(node)
    return resitev


# Naredi csv file




# Sim povprečje za vse (velike) grafe
columns = ["Percent", "Avg. efficiency", "Sim 10", "Sim 100", "Sim 1000"]
columns_removed = ["Percent", "Random", "Centered"]
data = {}                   # Za sim

# Grid
for i in [2, 3, 4, 5, 10, 20, 50, 100]:                                            # Spremeni stevilke
    for j in [1, 2, 3, 4, 5, 10, 20, 50, 100]:
        for k in [1, 2, 3, 4, 5, 10, 20, 50, 100]:
            # sim zanka
            for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:                     # Spremeni stevilke
                grid_data = []
                grid_global = []
                grid_centered = []
                for _ in range(1000):            #
                    grid = generate_3d_grid(i, j, k)
                    grid_1 = remove_random(generate_3d_grid(i,j,k), percent)
                    grid_2 = remove_centered(generate_3d_grid(i, j, k), percent)
                    grid_data.append(average_sim(grid, percent))
                    grid_global.append(global_efficiency(grid_1, grid))
                    grid_centered.append(global_efficiency(grid_2, grid))
                data["Grid {}x{}x{} at {}".format(i, j, k, percent)] = [percent, average_efficiency(grid), sum(grid_data[:10])/10, sum(grid_data[:100])/100, sum(grid_data)/1000]
                data_removed["Grid {}x{}x{} at {}".format(i, j, k, percent)] = [percent, sum(grid_global)/1000, sum(grid_centered)/1000]

# Tree
for i in range(2, 21): 
    tree = generate_binary(i)
    for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:                         # Spremeni stevilke
        tree_data = []
        tree_global= []
        tree_centered = []
        for _ in range(1000):            #
            tree_data.append(average_sim(tree, percent))
            tree_global.append(global_efficiency(remove_random(tree, percent), tree))
            tree_centered.append(global_efficiency(remove_centered(tree, percent), tree))
        data["Tree {} at {}".format(i, percent)] = [percent, average_efficiency(tree), sum(tree_data[:10])/10, sum(tree_data[:100])/100, sum(tree_data)/1000]
        data_removed["Tree {} at {}".format(i, percent)] = [percent, sum(tree_global)/1000, sum(tree_centered)/1000]

# Cycle
for i in [2, 3, 4, 5, 10, 20, 50, 100, 200, 300, 400, 500, 1000, 10000, 100000, 1000000]: 
    cycle = generate_cycle(i)
    for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:                         # Spremeni stevilke
        cycle_data = []
        cycle_global= []
        cycle_centered = []
        for _ in range(1000):        #
            cycle_data.append(average_sim(cycle, percent))
            cycle_global.append(global_efficiency(remove_random(cycle, percent), cycle))
            cycle_centered.append(global_efficiency(remove_centered(cycle, percent), cycle))
        data["Cycle {} at {}".format(i, percent)] = [percent, average_efficiency(cycle), sum(cycle_data[:10])/10, sum(cycle_data[:100])/100, sum(cycle_data)/1000]
        data_removed["Cycle {} at {}".format(i, percent)] = [percent, sum(cycle_global)/1000, sum(cycle_centered)/1000]


df = pandas.DataFrame.from_dict(data, orient='index', columns = columns)







# Nedelujoče povezave na gridih, drevesih in naključnih remove centered
cols = ["Random", "Centered"]
data_1 = {}
data_2 = {}
osnoven = generate_3d_grid(50, 50, 50)
osnoven_2 = generate_3d_grid(100, 100, 100)
for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:                 # Spremeni
    rand = remove_random(generate_3d_grid(10, 10, 10), percent)
    centered = remove_centered(generate_3d_grid(10, 10, 10), percent)
    data_1[percent] = [global_efficiency(rand, osnoven), global_efficiency(centered, osnoven)]
    random_2 = remove_random(generate_3d_grid(100, 100, 100), percent)
    centered_2 = remove_centered(generate_3d_grid(100, 100, 100), percent)
    data_2[percent] = [global_efficiency(random_2, osnoven_2), global_efficiency(centered_2, osnoven_2)]

df_1 = pandas.DataFrame.from_dict(data_1, orient='index', columns = cols)
df_2 = pandas.DataFrame.from_dict(data_2, orient='index', columns = cols)


data_1_bin = {}
data_2_bin = {}
osnoven_b = generate_binary(10)
osnoven_2_b = generate_binary(20)
for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:                 # Spremeni
    rand = remove_random(generate_binary(10), percent)
    centered = remove_centered(generate_binary(10), percent)
    data_1_bin[percent] = [global_efficiency(rand, osnoven_b), global_efficiency(centered, osnoven_b)]
    random_2 = remove_random(generate_binary(20), percent)
    centered_2 = remove_centered(generate_binary(20), percent)
    data_2_bin[percent] = [global_efficiency(random_2, osnoven_2_b), global_efficiency(centered_2, osnoven_2_b)]

df_1 = pandas.DataFrame.from_dict(data_1_bin, orient='index', columns = cols)
df_2 = pandas.DataFrame.from_dict(data_2_bin, orient='index', columns = cols)




