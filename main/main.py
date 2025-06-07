from loguru import logger
from graph.graph_constants import MODEL_METHOD
from star.star_algorithm import T_Star_Grid_Graphs

GRAPH_ORDER = 2
DYNAMIMC_COLORING_ORDER = 2
AVAILABLE_COLORS = 8
MAX_GRAPHS = 1

def has_repeated_edges(adjacency_list):
    """
    Check if a graph represented by an adjacency list has any repeated edges.
    In an undirected graph, (u,v) and (v,u) are considered the same edge.
    
    Args:
        adjacency_list (dict): A dictionary where keys are vertices and values are lists of adjacent vertices.
        
    Returns:
        bool: True if there are repeated edges, False otherwise.
    """
    # For each vertex, track which neighbors we've seen
    seen_neighbors = {v: set() for v in adjacency_list}
    
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            # For undirected graphs, we only need to check in one direction
            if vertex > neighbor:
                continue
                
            if neighbor in seen_neighbors[vertex]:
                # Found a duplicate edge
                return True
            seen_neighbors[vertex].add(neighbor)
            
    return False

if __name__ == "__main__":
    graph_class = T_Star_Grid_Graphs(GRAPH_ORDER, DYNAMIMC_COLORING_ORDER, AVAILABLE_COLORS)
    graph_class.define_graph(MAX_GRAPHS)

    for graph in graph_class.TOTAL_GRAPHS:
        if has_repeated_edges(graph.details.code.adjacency_list):
            logger.info(f'Graph {graph.details.coordinate.adjacency_list} has repeated edges')
    logger.info(f'Graphs with repeated edges: {len(graph_class.TOTAL_GRAPHS)}')
    logger.info(f'Graphs without repeated edges: {len(graph_class.TOTAL_GRAPHS) - len(graph_class.TOTAL_GRAPHS)}')
    
    # logger.info(f'Stack: {graph_class.PRIORITY_QUEUE.heap}')
    # logger.info(f'Total graphs: {len(graph_class.TOTAL_GRAPHS)}')
    # for i, g in enumerate(graph_class.TOTAL_GRAPHS):
    #     logger.info(f'Graph {i}: {g.details.coordinate.adjacency_list}')
    #     logger.info(f'Graph {i} border: {g.details.coordinate.border}')

    # logger.info(f'Queue size sequence: {graph_class.queue_size_sequence}')

    # colors = set()
    # for graph in graph_class.TOTAL_GRAPHS:
    #     solution_status = graph.linear_programming_model(model_name=MODEL_METHOD.ACR, previous_variables=None)
    #     colors_used = graph.coloring_assignment(coloring_function=None)
    #     colors.add(colors_used)
        # logger.info(f'')
        # if colors_used == 4:
        #     logging.info(f'Four colors: ')
        #     break

    # logger.info(f'Colors used: {colors}')
