from graph import Graph, Graph3D
import graph
from graph.visuals import plot_3d, plot_2d
import math
import random

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
    number_of_edges = randrange(n**(n-1))
    rand = Graph()
    for i in range(1, n):
        rand.add_node(i)
    while number_of_edges > 0:
        first = random.choice(rand.nodes())
        node = [nod for nod in rand.nodes() if nod != first]
        second = random.choice(node)
        rand.add_edge(first, second, 1)
        number_of_edges -= 1
    return random

a = generate_1xn(5)
print(random.choice(a.nodes()))    

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


def global_efficiency(graph):
    n = len(graph.nodes())
    ideal = generate_ideal(n)
    if n == 1:
        return 0
    return average_efficiency(graph)/average_efficiency(ideal)


def local_efficiency(graph):
    total = 0
    for node in graph.nodes():
        podgraf = graph.subgraph_from_nodes(graph.network_size(node, 1))
        podgraf.del_node(node)
        total += average_efficiency(podgraf)
    return total / len(graph.nodes())




# So far so good! :)
'''
for i in [2, 3, 4, 5, 10, 20]:
    print("Povprečna učinkovitost za " + str(i) + ": " + str(average_efficiency(generate_1xn(i)))) 
    print("Globalna učinkovitost za " + str(i) + ": " + str(global_efficiency(generate_1xn(i)))) 
    print("Lokalna učinkovitost za " + str(i) + ": " + str(local_efficiency(generate_1xn(i))))
'''
# The following functions calculate efficiencies by only considering a random subset of pairs rather than all possible pairs of vetrices.
# Functions are given an argument that tells them what percentage of pairs to select

def average_sim(graph, percent):
    pairs = set()
    while len(pairs) < min(len(graph.nodes())* (len(graph.nodes()) - 1) * percent, len(graph.nodes())* (len(graph.nodes()) - 1) * (1 - percent)):
        first = random.choice(graph.nodes())
        second = random.choice(graph.nodes())
        if first != second:
            pairs.add((first, second))
    if percent > 0.5:
        # missing part where you take complement of pairs
        pass
    total = 0
    for pair in pairs:
        total += 1 / graph.shortest_path(pair[0], pair[1])
    return total / len(pairs)

def global_sim(graph, percent):
    pairs = set()
    while len(pairs) < min(len(graph.nodes())* (len(graph.nodes()) - 1) * percent, len(graph.nodes())* (len(graph.nodes()) - 1) * (1 - percent)):
        first = random.choice(graph.nodes())
        second = random.choice(graph.nodes())
        if first != second:
            pairs.add((first, second))
    if percent > 0.5:
        # missing part where you take complement of pairs
        pass
    # Might change also:
    return average_sim(graph, percent)/average_sim(generate_ideal(len(graph.nodes())))

def local_sim(graph, percent):
    pass



