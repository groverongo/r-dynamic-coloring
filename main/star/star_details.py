from dataclasses import dataclass
from typing import Dict, Set, List, Tuple
import heapq

@dataclass
class Star_Graph_Information():
    graph: Dict[int, List[int]]
    border: Set[int]
    triads: List[Tuple[int, int, int]]
    triads_history: List[Tuple[int, int, int]]

class Graph_Stack():

    @dataclass
    class Graph_Stack_Element(Star_Graph_Information):
        triad_index: int
        
        def __lt__(self, other):
            return len(self.triads) < len(other.triads)
    
    def __init__(self):
        self.heap: List[Graph_Stack.Graph_Stack_Element] = []

    def push(self, element: Graph_Stack_Element):
        heapq.heappush(self.heap, element)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)
        raise IndexError("pop from empty heap")

    def peek(self):
        if self.heap:
            return self.heap[0]
        raise IndexError("peek at empty heap")

    def is_empty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)

    def to_json(self):
        return {
            "stack": [element.to_json() for element in self.heap]
        }