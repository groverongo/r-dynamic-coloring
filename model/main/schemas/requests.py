from typing import Dict, List, Literal, Tuple, Union, Optional
from pydantic import BaseModel

class BaseColoringRequest(BaseModel):
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']
    k: int
    r: int

class BaseColoringBatchRequest(BaseModel):
    method: Literal['ACR', 'ACR_H', 'ACR_R', 'ACR_RH']
    k_range: Optional[Tuple[int, int]] = None
    r_range: Tuple[int, int]

class ColoringGraphRequest(BaseColoringRequest):
    graph_type: Literal['adjacency_list', 'adjacency_matrix']
    graph: Union[Dict[int, List[int]], List[List[int]]]

class CirculantRequest(BaseColoringRequest):
    n: int
    connections: List[int]

class CirculantBatchRequest(BaseColoringBatchRequest):
    n_range: Tuple[int, int]
    connections: List[int]
    k: int

class AntiprismRequest(BaseColoringRequest):
    n: int

class AntiprismBatchRequest(BaseColoringBatchRequest):
    n_range: Tuple[int, int]
    k: int

class Planar3TreeRequest(BaseColoringRequest):
    n: int
    
class Planar3TreeBatchRequest(BaseColoringBatchRequest):
    n_range: Tuple[int, int]
    k: int