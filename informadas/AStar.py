from abstracciones.best_first_graph_search import best_first_graph_search
from abstracciones.Node import Node

def AStar(problem, f):
    return best_first_graph_search(problem, f)