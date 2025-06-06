from loguru import logger
from star.star_algorithm import T_Star_Grid_Graphs


if __name__ == "__main__":
    graph = T_Star_Grid_Graphs(3, 2, 8)
    graph.define_graph()

    logger.info(f'Stack: {graph.PRIORITY_QUEUE.heap}')
    logger.info(f'Total graphs: {len(graph.TOTAL_GRAPHS)}')
    for i, g in enumerate(graph.TOTAL_GRAPHS):
        logger.info(f'Graph {i}: {g.details.coordinate.adjacency_list}')
