from copy import deepcopy
from typing import List
from graph.graph_coloring import T_Grid_Graph
from .star_utils import middle_vertex_presence_filter, obtain_candidate_vertex, update_grid
from .star_types import INDEX_ACCESS_TRIAD, Star_Triad_Type
from .star_details import Graph_Priority_Queue
from loguru import logger

class T_Star_Grid_Graphs():
    def __init__(self, n: int, r: int, k: int):
        self.BASE_GRAPH: T_Grid_Graph = T_Grid_Graph(n, r, k)
        # List of T_Grid_Graph is actually T_Star_Graph
        self.TOTAL_GRAPHS: List[T_Grid_Graph] = []
        self.TOTAL_GRAPHS_HISTORY: List[List[Star_Triad_Type]] = []

    def validate_max_graphs(self, max_graphs: int):
        if max_graphs == -1:
            return True
        return len(self.TOTAL_GRAPHS) < max_graphs

    def define_new_edges(self, max_graphs: int):
        code_to_coordinate = self.BASE_GRAPH.details.code.to_other

        self.PRIORITY_QUEUE = Graph_Priority_Queue()
        for triad_index in range(len(self.BASE_GRAPH.details.code.triad_candidates)):
            self.PRIORITY_QUEUE.push(Graph_Priority_Queue.Graph_Priority_Queue_Element(
                graph=deepcopy(self.BASE_GRAPH.details.code.adjacency_list),
                border=deepcopy(self.BASE_GRAPH.details.code.border),
                triads=deepcopy(self.BASE_GRAPH.details.code.triad_candidates),
                triad_index=triad_index,
                triads_history=[]
            ))

        self.queue_size_sequence: List[int] = [len(self.PRIORITY_QUEUE.heap)]

        while not self.PRIORITY_QUEUE.is_empty() and self.validate_max_graphs(max_graphs):
            # logger.debug(f'Current elements: {PRIORITY_QUEUE.heap}')
            element = self.PRIORITY_QUEUE.pop()
            self.queue_size_sequence.append(len(self.PRIORITY_QUEUE.heap))

            # logger.debug(f'Available triads: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads))}')
            

            if len(element.triads) <= 3:
                t_star_graph = update_grid(element, deepcopy(self.BASE_GRAPH))
                self.TOTAL_GRAPHS.append(t_star_graph)
                self.TOTAL_GRAPHS_HISTORY.append(element.triads_history)
                continue

            selected_triad = element.triads[element.triad_index]
            element.triads_history.append(selected_triad)

            # logger.debug(f'Selected triad: {list(map(lambda v: code_to_coordinate[v], selected_triad))}')

            vertex_1_candidates: List[Star_Triad_Type] = []
            vertex_2_candidates: List[Star_Triad_Type] = []

            for triad in element.triads:
                if triad == selected_triad: continue
                if selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value] in triad:
                    vertex_1_candidates.append(triad)
                elif selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value] in triad:
                    vertex_2_candidates.append(triad)

            # logger.debug(f'Vertex 1 candidates: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), vertex_1_candidates))}')
            # logger.debug(f'Vertex 2 candidates: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), vertex_2_candidates))}')

            triad_vertex_1: Star_Triad_Type = [
                obtain_candidate_vertex(selected_triad, vertex_1_candidates, INDEX_ACCESS_TRIAD.VERTEX_1),
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value],
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]
            ]

            triad_vertex_2: Star_Triad_Type = [
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value],
                selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value],
                obtain_candidate_vertex(selected_triad, vertex_2_candidates, INDEX_ACCESS_TRIAD.VERTEX_2)
            ]

            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value])
            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value])

            element.triads.pop(element.triad_index)
            element.triads = list(filter(lambda triad: middle_vertex_presence_filter(triad, selected_triad) == -1, element.triads))
            element.triads.extend([triad_vertex_1, triad_vertex_2])

            element.border.remove(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])

            # logger.debug(f'Result: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads))}')

            for index_triad in range(len(element.triads)):
                self.PRIORITY_QUEUE.push(Graph_Priority_Queue.Graph_Priority_Queue_Element(
                    graph=deepcopy(element.graph),
                    border=deepcopy(element.border),
                    triads=deepcopy(element.triads),
                    triad_index=index_triad,
                    triads_history=deepcopy(element.triads_history)
                ))
        
        self.queue_size_sequence.append(len(self.PRIORITY_QUEUE.heap))
        
    def define_graph(self, max_graphs: int = -1):
        self.BASE_GRAPH.define_graph()
        self.define_new_edges(max_graphs)

        