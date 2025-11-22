from typing import Dict, List, Literal, Tuple, Union
from pydantic import BaseModel

class BaseColoringRequest(BaseModel):
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']
    k: int
    r: int

class BaseColoringBatchRequest(BaseModel):
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']
    k_range: Tuple[int, int]
    r_range: Tuple[int, int]

class ColoringGraphRequest(BaseColoringRequest):
    graph_type: Literal['adjacency_list', 'adjacency_matrix']
    graph: Union[Dict[int, List[int]], List[List[int]]]

class AntiprismRequest(BaseColoringRequest):
    n: int

class AntiprismBatchRequest(BaseColoringBatchRequest):
    n_range: Tuple[int, int]
    k: int
