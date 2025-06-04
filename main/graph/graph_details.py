from dataclasses import dataclass
from typing import TypeVar, Generic, List, Tuple, Dict

from numpy.typing import NDArray
from pulp import LpProblem, LpVariable

from .graph_types import VertexType

T = TypeVar('T')
U = TypeVar('U')
@dataclass
class Graph_Details:
    @dataclass
    class Graph_Info(Generic[T,U]):
        vertices: List[T]
        edges: List[Tuple[T, T]]
        adjacency_list: Dict[T, List[T]]
        to_other: Dict[T, U]
        border: List[T]
        triad_candidates: List[Tuple[T, T, T]]

    @dataclass
    class Misc:
        degree: Dict[int, int]

    misc: Misc
    code: Graph_Info[VertexType.Code, VertexType.Coordinate]
    coordinate: Graph_Info[VertexType.Coordinate, VertexType.Code]

@dataclass
class Coloring_Solution:
    model: LpProblem
    w: NDArray[LpVariable]
    x: NDArray[NDArray[LpVariable]]
    q: NDArray[NDArray[LpVariable]]

@dataclass
class Graph_Colors:
    code: Dict[VertexType.Code, int]
    coordinate: Dict[VertexType.Coordinate, int]
    used_colors: int