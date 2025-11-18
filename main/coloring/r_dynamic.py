from loguru import logger
from numpy.typing import NDArray
from .model import Coloring_Solution, MODEL_METHOD
import numpy as np
from pulp import LpVariable, LpMinimize, LpProblem, lpSum, GLPK
from typing import Dict, List, Tuple, TypeVar

T = TypeVar('T')
def linear_programming_model(
    adjacency_list: Dict[T, List[T]],
    model_name: MODEL_METHOD,
    previous_variables: Coloring_Solution = None,
    write_lp_path: str = None,
    k: int = None,
    r: int = None,
    name: str = "Coloring",
):
    if model_name not in [MODEL_METHOD.ACR, MODEL_METHOD.ACR_H, MODEL_METHOD.ACR_R, MODEL_METHOD.ACR_RH] and model_name not in [MODEL_METHOD.ACR.value, MODEL_METHOD.ACR_H.value, MODEL_METHOD.ACR_R.value, MODEL_METHOD.ACR_RH.value]:
        raise ValueError(f"model_name '{model_name}' must be '{MODEL_METHOD.ACR}', '{MODEL_METHOD.ACR_H}', '{MODEL_METHOD.ACR_R}' or '{MODEL_METHOD.ACR_RH}'")

    if k is None:
        raise ValueError("k must be specified")

    if r is None:
        raise ValueError("r must be specified")

    edges: List[Tuple[T, T]] = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in adjacency_list for final_vertex in adjacency_list[initial_vertex]]))
    degrees: Dict[T, int] = {vertex: len(adjacency_list[vertex]) for vertex in adjacency_list}

    w: NDArray[LpVariable] = np.array([LpVariable(f"w({k_i})", 0, 1, cat="Binary") for k_i in range(k)])
    x: NDArray[NDArray[LpVariable]] = np.array([[LpVariable(name=f"x({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])
    q: NDArray[NDArray[LpVariable]] = np.array([[LpVariable(name=f"q({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])

    model = LpProblem(name=f'{name}', sense=LpMinimize)
    model += lpSum(w)

    if previous_variables and (model_name in [MODEL_METHOD.ACR_R, MODEL_METHOD.ACR_RH] or model_name in [MODEL_METHOD.ACR_R.value, MODEL_METHOD.ACR_RH.value]):
        for k_i in range(k):
            if previous_variables.w[k_i].varValue == 0:
                break
            model += w[k_i] == previous_variables.w[k_i].varValue
        for v in range(previous_variables.x.shape[0]):
            for k_i in range(k):
                model += x[v, k_i] == previous_variables.x[v, k_i].varValue

    # Constraint 1
    for v in adjacency_list.keys():
        model += lpSum(x[v]) == 1
    # Constraint 2
    for (u, v) in edges:
        for k_i in range(k):
            if (model_name in [MODEL_METHOD.ACR_H, MODEL_METHOD.ACR_RH] or model_name in [MODEL_METHOD.ACR_H.value, MODEL_METHOD.ACR_RH.value]):
                model += x[u, k_i] + x[v, k_i] <= 1
            else:
                model += x[u, k_i] + x[v, k_i] <= w[k_i]
    if model_name in [MODEL_METHOD.ACR, MODEL_METHOD.ACR_R] or model_name in [MODEL_METHOD.ACR.value, MODEL_METHOD.ACR_R.value]:
        # Constraint 3
        for k_i  in range(k):
            model += w[k_i] <= lpSum(x[:, k_i])
        # Constraint 4
        for k_i in range(1, k):
            model += w[k_i - 1] >= w[k_i]
    # Constraint 5
    for v, deg in degrees.items():
        model += lpSum(q[v]) >= min(r, deg)
    # Constraint 6
    for v, n_v in adjacency_list.items():
        for k_i in range(k):
            model += lpSum(x[n_v, k_i]) >= q[v, k_i]
    # Constraint 7
    for v, n_v in adjacency_list.items():
        for u in n_v:
            for k_i in range(k):
                model += q[v, k_i] >= x[u, k_i]

    if write_lp_path:
        model.writeLP(write_lp_path)

    model.solve(solver=GLPK(msg=False))

    return Coloring_Solution(model=model, w=w, x=x, q=q)