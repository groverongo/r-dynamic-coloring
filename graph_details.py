from typing import TypeVar, Generic, List, Tuple, Dict

T = TypeVar('T')

U = TypeVar('U')

class Graph_Details:
    class Graph_Info(Generic[T,U]):
        def __init__(
            self,
            vertices: List[T],
            edges: List[Tuple[T, T]],
            adjacency_list: Dict[T, List[T]],
            to_other: Dict[T, U],
            border: List[T],
            triad_candidates: List[Tuple[T, T, T]]
        ):
            self.vertices = vertices
            self.edges = edges
            self.adjacency_list = adjacency_list
            self.to_other = to_other
            self.border = border
            self.triad_candidates = triad_candidates

    class Misc:
        def __init__(self, degree: Dict[int, int]):
            self.degree = degree

    def __init__(self, misc: Misc, code: Graph_Info[int, Tuple[int, int]], coordinate: Graph_Info[Tuple[int, int], int]):
        self.misc = misc
        self.code = code
        self.coordinate = coordinate