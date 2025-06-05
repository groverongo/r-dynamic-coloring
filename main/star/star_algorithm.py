from copy import deepcopy
from typing import List, Union
from graph.graph_coloring import T_Grid_Graph
from .star_types import INDEX_ACCESS_TRIAD, Star_Triad_Type
from .star_details import Graph_Stack, Star_Graph_Information

class T_Star_Grid_Graph(T_Grid_Graph):
    def __init__(self, n: int, r: int, k: int):
        super().__init__(n, r, k)

        self.TOTAL_GRAPHS: List[Star_Graph_Information] = []

    def obtain_candidate_vertex(self, selected_triad: Star_Triad_Type, triad_candidates: List[Star_Triad_Type], terminal_vertex: Union[INDEX_ACCESS_TRIAD.VERTEX_1, INDEX_ACCESS_TRIAD.VERTEX_2]):
        for triad in triad_candidates:
            if selected_triad[terminal_vertex.value] == triad[INDEX_ACCESS_TRIAD.MIDDLE.value]:
                if selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value] == triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]:
                    return triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]
                else:
                    return triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]
            else:
                return triad[INDEX_ACCESS_TRIAD.MIDDLE.value]

    def middle_vertex_presence_filter(self, triad: Star_Triad_Type):
        try:
            return triad.index(triad[INDEX_ACCESS_TRIAD.MIDDLE.value])
        except ValueError:
            return -1

    def define_new_edges(self):
        code_adjacency_list = self.details.code.adjacency_list
        border_code = self.details.code.border
        triad_candidates_code = self.details.code.triad_candidates
        code_to_coordinate = self.details.code.to_other

        STACK = Graph_Stack()
        for triad_index in range(len(triad_candidates_code)):
            STACK.push(Graph_Stack.Graph_Stack_Element(
                graph=deepcopy(code_adjacency_list),
                border=deepcopy(border_code),
                triads=deepcopy(triad_candidates_code),
                triad_index=triad_index,
                triads_history=[]
            ))

        while not STACK.is_empty():
            print('Current elements:', STACK.heap)
            element = STACK.pop()

            print('Available triads:', list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads)))
            

            if len(element.triads) <= 3:
                self.TOTAL_GRAPHS.append(element)
                return

            selected_triad = element.triads[element.triad_index]
            element.triads_history.append(selected_triad)

            print('Selected triad:', list(map(lambda v: code_to_coordinate[v], selected_triad)))

            vertex_1_candidates: List[Star_Triad_Type] = []
            vertex_2_candidates: List[Star_Triad_Type] = []

            for triad in element.triads:
                if triad == selected_triad: continue
                if selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value] in triad:
                    vertex_1_candidates.append(triad)
                elif selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value] in triad:
                    vertex_2_candidates.append(triad)

            print('Vertex 1 candidates:', list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), vertex_1_candidates)))
            print('Vertex 2 candidates:', list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), vertex_2_candidates)))

            triad_vertex_1: Star_Triad_Type = [
                self.obtain_candidate_vertex(selected_triad, vertex_1_candidates, INDEX_ACCESS_TRIAD.VERTEX_1),
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value],
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]
            ]

            triad_vertex_2: Star_Triad_Type = [
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value],
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value],
                self.obtain_candidate_vertex(selected_triad, vertex_2_candidates, INDEX_ACCESS_TRIAD.VERTEX_2)
            ]

            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value])
            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value])

            element.triads.pop(element.triad_index)
            element.triads = list(filter(lambda triad: self.middle_vertex_presence_filter(triad) == -1, element.triads))
            element.triads.extend([triad_vertex_1, triad_vertex_2])

            element.border.remove(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])

            print('Result:', list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads)))

            for index_triad in range(len(element.triads)):
                STACK.push(Graph_Stack.Graph_Stack_Element(
                    graph=deepcopy(element.graph),
                    border=deepcopy(element.border),
                    triads=deepcopy(element.triads),
                    triad_index=index_triad,
                    triads_history=deepcopy(element.triads_history)
                ))
        

    def define_graph(self):
        super().define_graph()
        self.define_new_edges()
        print('Total graphs:', len(self.TOTAL_GRAPHS))

        