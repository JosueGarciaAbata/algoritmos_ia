from abstracciones.best_first_graph_search import best_first_graph_search

def uniform_cost_search(problem, display=False):
    """
    Búsqueda de costo uniforme.

    Expande siempre el nodo con menor costo acumulado (`path_cost`).
    Es un caso particular de best-first graph search donde:

        f(node) = node.path_cost
    """
    
    return best_first_graph_search(problem, lambda node: node.path_cost, display)