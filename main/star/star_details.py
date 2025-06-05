from dataclasses import dataclass
from typing import Dict, Set, List, Tuple

@dataclass
class Star_Graph_Information():
    graph: Dict[int, List[int]]
    border: Set[int]
    triads: List[Tuple[int, int, int]]
    triads_history: List[Tuple[int, int, int]]

@dataclass
class Graph_Stack():

    @dataclass
    class Graph_Stack_Element(Star_Graph_Information):
        triad_index: int
    
    stack: List[Graph_Stack_Element] = []

    def push(self, element: Graph_Stack_Element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)

    def to_json(self):
        return {
            "stack": [element.to_json() for element in self.stack]
        }