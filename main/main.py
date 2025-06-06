from loguru import logger
from graph.graph_constants import MODEL_METHOD
from star.star_algorithm import T_Star_Grid_Graphs

GRAPH_ORDER = 2

if __name__ == "__main__":
    graph_class = T_Star_Grid_Graphs(GRAPH_ORDER, 2, 8)
    graph_class.define_graph(20)

    logger.info(f'Stack: {graph_class.PRIORITY_QUEUE.heap}')
    logger.info(f'Total graphs: {len(graph_class.TOTAL_GRAPHS)}')
    for i, g in enumerate(graph_class.TOTAL_GRAPHS):
        logger.info(f'Graph {i}: {g.details.coordinate.adjacency_list}')
        logger.info(f'Graph {i} border: {g.details.coordinate.border}')
        logger.info(f'Graph {i} triads: {g.details.coordinate.triad_candidates}')

    logger.info(f'Queue size sequence: {graph_class.queue_size_sequence}')

    # for graph in graph_class.TOTAL_GRAPHS:
    #     graph.linear_programming_model(model_name=MODEL_METHOD.ACR, previous_variables=None)
    #     graph.coloring_assignment(coloring_function=None)
