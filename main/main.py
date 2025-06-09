from loguru import logger
from graph.graph_constants import MODEL_METHOD
from star.star_types import RESULTANT_GRAPHS
from star.star_algorithm import T_Star_Grid_Graphs
from tqdm import tqdm
from utils.check_multigraph import has_repeated_edges
import numpy as np

GRAPH_ORDER = 3
DYNAMIMC_COLORING_ORDER = 4
AVAILABLE_COLORS = 15
MAX_GRAPHS = 200
RESULTANT = RESULTANT_GRAPHS.FULL_SET

if __name__ == "__main__":
    graph_class = T_Star_Grid_Graphs(GRAPH_ORDER, DYNAMIMC_COLORING_ORDER, AVAILABLE_COLORS)
    graph_class.define_graph(MAX_GRAPHS, RESULTANT)

    repeated_edges_count = 0

    for i, graph in enumerate(graph_class.TOTAL_GRAPHS):
        if has_repeated_edges(graph.details.code.adjacency_list):
            logger.info(f'Graph {i} {graph.details.coordinate.adjacency_list} has repeated edges')
            repeated_edges_count += 1
        else:
            logger.info(f'Graph {i}: {graph.details.coordinate.adjacency_list}')
    logger.info(f'Graphs with repeated edges: {repeated_edges_count}')
    logger.info(f'Graphs without repeated edges: {len(graph_class.TOTAL_GRAPHS) - repeated_edges_count}')

    colors: list[int] = []
    for graph in tqdm(graph_class.TOTAL_GRAPHS):
        solution_status = graph.linear_programming_model(
            model_name=MODEL_METHOD.ACR, 
            previous_variables=None,
            write_lp_path=f"../graphs/Tstar{GRAPH_ORDER}Max-{DYNAMIMC_COLORING_ORDER}.lp"
        )
        
        colors_used = graph.coloring_assignment(coloring_function=None)
        colors.append(colors_used)
        # logger.info(f'Colors used: {colors_used}')
        # if colors_used == 5:
        #     logger.info(f'Five colors: {graph.details.coordinate.adjacency_list}')
            # break

    logger.info(f'Colors used: {set(colors)}')
