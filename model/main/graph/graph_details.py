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

        def to_json(self):
            def tuple_to_str(item):
                if isinstance(item, tuple):
                    return f"({item[0]},{item[1]})"
                return item

            return {
                "vertices": self.vertices,
                "edges": self.edges,
                "adjacency_list": {tuple_to_str(k): v for k, v in self.adjacency_list.items()},
                "to_other": {tuple_to_str(k): v for k, v in self.to_other.items()},
                "border": self.border,
            }

    @dataclass
    class Misc:
        degree: Dict[int, int]

        def to_json(self):
            return {
                "degree": self.degree
            }

    misc: Misc
    code: Graph_Info[VertexType.Code, VertexType.Coordinate]
    coordinate: Graph_Info[VertexType.Coordinate, VertexType.Code]

    def to_json(self):
        return {
            "misc": self.misc.to_json(),
            "code": self.code.to_json(),
            "coordinate": self.coordinate.to_json()
        }

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

    def to_json(self):
        def tuple_to_str(item):
            if isinstance(item, tuple):
                return f"({item[0]},{item[1]})"
            return item
        return {
            "code": {tuple_to_str(k): v for k, v in self.code.items()},
            "coordinate": {tuple_to_str(k): v for k, v in self.coordinate.items()},
            "used_colors": self.used_colors
        }
        