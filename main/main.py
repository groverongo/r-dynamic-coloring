from typing import Dict, List, Literal, Tuple, Union
from loguru import logger
from pydantic import BaseModel
from graph.graph_constants import MODEL_METHOD
from coloring.r_dynamic import linear_programming_model
from utils.antiprism import create_antiprism_adjacency_matrix
from utils.solve_graphs import solve_full_set, solve_max_degree
from fastapi import FastAPI
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

GRAPH_ORDER_START = 3 # T_n
GRAPH_ORDER_END = 3 # T_n
DYNAMIMC_COLORING_ORDER = 3 # r
AVAILABLE_COLORS = 8 # k
MAX_GRAPHS = -1#200 
SAMPLE_GRAPHS = 3#1
OUTPUT_DIRECTORY = "../graphs/batches"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ColoringGraphRequest(BaseModel):
    method: str 
    k: int
    r: int
    graph_type: Literal['adjacency_list', 'adjacency_matrix']
    graph: Union[Dict[int, List[int]], List[List[int]]]

def adjacency_matrix_to_adjacency_list(graph: List[List[int]]) -> Dict[int, List[int]]:
    return {i: [j for j in range(len(graph)) if graph[i][j] == 1] for i in range(len(graph))}


@app.post("/")
def assign_colors(request: ColoringGraphRequest):

    if request.graph_type == 'adjacency_matrix':
        request.graph = adjacency_matrix_to_adjacency_list(request.graph)

    solution = linear_programming_model(adjacency_list=request.graph, model_name=request.method, k=request.k, r=request.r)

    logger.info(f'Solution: {solution}')

    color_assignment_code = {v: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(solution.x)}

    return {"coloring": color_assignment_code}


class AntiprismRequest(BaseModel):
    n: int
    r: int
    k: int
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']

@app.post("/circulant/antiprism")
def antiprism_assignment(request: AntiprismRequest):

    logger.info(f'Antiprism Request: {request}')
    
    adjacency_matrix = create_antiprism_adjacency_matrix(request.n)
    adjacency_list = adjacency_matrix_to_adjacency_list(adjacency_matrix)

    logger.info(f'Adjacency List: {adjacency_list}')

    solution = linear_programming_model(adjacency_list=adjacency_list, model_name=request.method, k=request.k, r=request.r)
    logger.info(f'Solution: {solution.x}')
    logger.info(f'Solution: {list(map(lambda x_vc: x_vc.varValue, solution.w))}')

    color_assignment_code = {v: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(solution.x)}

    return {"coloring": color_assignment_code}


class AntiprismBatchRequest(BaseModel):
    r_range: Tuple[int, int]
    n_range: Tuple[int, int]
    k: int
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']

@app.post("/batch/circulant/antiprism")
def antiprism_batch_assignment(request: AntiprismBatchRequest):
    
    logger.info(f'Antiprism Batch Request: {request}')

    # first key: r, second key: n, value: color_assignment_code
    solutions_object = {}
    
    for r in range(request.r_range[0], request.r_range[1] + 1):
        for n in range(request.n_range[0], request.n_range[1] + 1):

            logger.info(f'Antiprism Batch Request: r={r}, n={n}')

            adjacency_matrix = create_antiprism_adjacency_matrix(n)
            adjacency_list = adjacency_matrix_to_adjacency_list(adjacency_matrix)

            try:
                solution = linear_programming_model(adjacency_list=adjacency_list, model_name=request.method, k=request.k, r=r)
            except Exception as e:
                logger.error(f'Error: {e}')
                return f'Error: {e} on r={r}, n={n}'

            color_assignment_code = {v: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(solution.x)}

            solutions_object[r] = solutions_object.get(r, {})
            solutions_object[r][n] = color_assignment_code

    return solutions_object

# if __name__ == "__main__":
    
    # response = solve_full_set(
    #     dynamic_coloring_order=DYNAMIMC_COLORING_ORDER,
    #     available_colors=AVAILABLE_COLORS,
    #     start_order=GRAPH_ORDER_START,
    #     end_order=GRAPH_ORDER_END,
    #     max_graphs=MAX_GRAPHS,
    #     sample_graphs=SAMPLE_GRAPHS,
    #     output_directory=OUTPUT_DIRECTORY
    # )

    # logger.info(f'Solutions: {response}')