from dataclasses import dataclass
from typing import Any, Dict, Tuple

class VertexType:
    Coordinate = Tuple[int, int]
    Code = int

class EdgeType:
    Coordinate = Tuple[VertexType.Coordinate, VertexType.Coordinate]
    Code = Tuple[VertexType.Code, VertexType.Code]

@dataclass
class SolutionCheckResponse:
    success: bool
    constraint: int
    expression: str
    variables: Dict[str, Any]
    