from typing import Tuple

class VertexType:
    Coordinate = Tuple[int, int]
    Code = int

class EdgeType:
    Coordinate = Tuple[VertexType.Coordinate, VertexType.Coordinate]
    Code = Tuple[VertexType.Code, VertexType.Code]