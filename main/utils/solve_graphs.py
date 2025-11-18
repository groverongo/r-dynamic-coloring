from loguru import logger
from graph.graph_constants import MODEL_METHOD
from utils.check_multigraph import has_repeated_edges
from star.star_algorithm import T_Star_Grid_Graphs
from star.star_types import RESULTANT_GRAPHS
from tqdm import tqdm
import random

random.seed(2)

def solve_max_degree(
    dynamic_coloring_order: int,
    available_colors: int,
    start_order: int,
    end_order: int = None,
    max_graphs: int = -1,
    output_directory: str = None,
    sample_graphs: int = None
):
    if end_order == None:
        end_order = start_order

    response = {}

    for order in tqdm(range(start_order, end_order + 1)):
        graph_class = T_Star_Grid_Graphs(order, dynamic_coloring_order, available_colors)
        graph_class.define_graph(max_graphs, RESULTANT_GRAPHS.MAX_DEGREE)

        logger.info("Total graphs: ", len(graph_class.TOTAL_GRAPHS))

        if sample_graphs:
            graph_class.TOTAL_GRAPHS = random.sample(graph_class.TOTAL_GRAPHS, sample_graphs)

        colors: list[int] = []
        for i, graph in tqdm(enumerate(graph_class.TOTAL_GRAPHS)):

            if has_repeated_edges(graph.details.code.adjacency_list):
                logger.info(f'Graph {i} {graph.details.coordinate.adjacency_list} has repeated edges')
                continue

            solution_status = graph.linear_programming_model(
                model_name=MODEL_METHOD.ACR, 
                previous_variables=None,
            )

            if solution_status != "Optimal":
                raise ValueError(f'Graph {i} {graph.details.coordinate.adjacency_list} is  {solution_status}')
            
            colors_used = graph.coloring_assignment(coloring_function=None)
            if output_directory:
                graph.graph_image(
                    output_file=f"TStar{order}-{dynamic_coloring_order}-{i}.png", 
                    output_directory=output_directory
                )
            colors.append(colors_used)

        distinct_colors = set(colors)

        response[order] = list(distinct_colors)
            
    return response

def solve_full_set(
    dynamic_coloring_order: int,
    available_colors: int,
    start_order: int,
    end_order: int = None,
    max_graphs: int = -1,
    output_directory: str = None,
    sample_graphs: int = None
):

    if end_order == None:
        end_order = start_order

    response = {}

    for order in tqdm(range(start_order, end_order + 1)):
        graph_class = T_Star_Grid_Graphs(order, dynamic_coloring_order, available_colors)
        graph_class.define_graph(max_graphs, RESULTANT_GRAPHS.FULL_SET)

        logger.info("Total graphs: ", graph_class.TOTAL_GRAPHS)
        if sample_graphs:
            graph_class.TOTAL_GRAPHS = random.sample(graph_class.TOTAL_GRAPHS, sample_graphs)

        print(len(graph_class.TOTAL_GRAPHS))

        colors: list[int] = []
        for i, graph in tqdm(enumerate(graph_class.TOTAL_GRAPHS)):

            if has_repeated_edges(graph.details.code.adjacency_list):
                logger.info(f'Graph {i} {graph.details.coordinate.adjacency_list} has repeated edges')
                continue

            solution_status = graph.linear_programming_model(
                model_name=MODEL_METHOD.ACR, 
                previous_variables=None,
            )

            if solution_status != "Optimal":
                raise ValueError(f'Graph {i} {graph.details.coordinate.adjacency_list} is  {solution_status}')
            
            colors_used = graph.coloring_assignment(coloring_function=None)
            if output_directory:
                graph.graph_image(
                    output_file=f"TStar{order}-{dynamic_coloring_order}-{i}.png", 
                    output_directory=output_directory
                )
            colors.append(colors_used)

        distinct_colors = set(colors)

        response[order] = list(distinct_colors)
            
    return response