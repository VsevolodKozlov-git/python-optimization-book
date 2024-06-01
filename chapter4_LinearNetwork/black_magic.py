import numpy as np
from scipy.sparse.csgraph import shortest_path

import random

def initialize_graph(num_vertices, edge_probability=0.3, max_weight=10):
    """
    Initialize a 2D matrix representation of a graph.

    :param num_vertices: Number of vertices in the graph.
    :param edge_probability: Probability of an edge existing between two vertices.
    :param max_weight: Maximum weight of an edge.
    :return: A 2D matrix representing the graph.
    """
    graph = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j and random.random() < edge_probability:
                graph[i][j] = random.randint(1, max_weight)

    return graph

def modify_graph(graph):
    """
    Modify the graph to ensure that there's a path from the start (vertex 0) to the end (last vertex).
    :param graph: The original graph matrix.
    :return: Modified graph matrix.
    """
    num_vertices = len(graph)
    # Ensure there's at least one outgoing edge from the start and one incoming edge to the end
    graph[0][random.randint(1, num_vertices - 1)] = random.randint(1, 10)
    graph[random.randint(0, num_vertices - 2)][num_vertices - 1] = random.randint(1, 10)
    return graph
if __name__ == '__main__':
    graph = initialize_graph(5)
# Modify the graph to ensure connectivity from start to end
    modified_graph = modify_graph(graph)

# Convert None to np.inf for the shortest path calculation
    graph_matrix = np.array([[float('inf') if x is None else x for x in row] for row in modified_graph])

    # Calculate the shortest path from the first vertex (0) to the last vertex
    distance_matrix, predecessors = shortest_path(csgraph=graph_matrix, directed=True, return_predecessors=True)
    shortest_path_length = distance_matrix[0][-1]

    print(modified_graph)
    print(shortest_path_length)