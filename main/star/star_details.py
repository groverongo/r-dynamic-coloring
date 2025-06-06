from dataclasses import dataclass
from typing import Dict, Set, List, Tuple
import heapq

@dataclass
class Star_Graph_Information():
    graph: Dict[int, List[int]]
    border: List[int]
    border_target_history: List[int]

class Graph_Priority_Queue():

    @dataclass
    class Graph_Priority_Queue_Element(Star_Graph_Information):
        border_target_index: int

        def __lt__(self, other):
            return len(self.border) < len(other.border)
    
    def __init__(self):
        self.heap: List[Graph_Priority_Queue.Graph_Priority_Queue_Element] = []

    def push(self, element: Graph_Priority_Queue_Element):
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