from typing import Dict, List, Literal, Tuple, Union
from pydantic import BaseModel

class ColoringGraphRequest(BaseModel):
    method: str 
    k: int
    r: int
    graph_type: Literal['adjacency_list', 'adjacency_matrix']
    graph: Union[Dict[int, List[int]], List[List[int]]]

class AntiprismRequest(BaseModel):
    n: int
    r: int
    k: int
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']

class AntiprismBatchRequest(BaseModel):
    r_range: Tuple[int, int]
    n_range: Tuple[int, int]
    k: int
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']
