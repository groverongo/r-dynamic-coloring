from copy import deepcopy
from typing import List
from graph.graph_coloring import T_Grid_Graph
from .star_utils import update_grid, verify_not_adjacent
from .star_types import INDEX_ACCESS_TRIAD, RESULTANT_GRAPHS, Star_Triad_Type
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

    def define_full_graphs(self, max_graphs: int):
        code_to_coordinate = self.BASE_GRAPH.details.code.to_other

        self.PRIORITY_QUEUE = Graph_Priority_Queue()
        for border_target_index in range(len(self.BASE_GRAPH.details.code.border)):
            evaluation_triad: Star_Triad_Type = [
                self.BASE_GRAPH.details.code.border[(border_target_index - 1) % len(self.BASE_GRAPH.details.code.border)],
                self.BASE_GRAPH.details.code.border[border_target_index],
                self.BASE_GRAPH.details.code.border[(border_target_index + 1) % len(self.BASE_GRAPH.details.code.border)]
            ]

            if not verify_not_adjacent(evaluation_triad, self.BASE_GRAPH.details.code.adjacency_list, self.BASE_GRAPH.n):
                continue

            self.PRIORITY_QUEUE.push(Graph_Priority_Queue.Graph_Priority_Queue_Element(
                graph=deepcopy(self.BASE_GRAPH.details.code.adjacency_list),
                border=deepcopy(self.BASE_GRAPH.details.code.border),
                border_target_index=border_target_index,
                border_target_history=[]
            ))

        self.queue_size_sequence: List[int] = [len(self.PRIORITY_QUEUE.heap)]

        while not self.PRIORITY_QUEUE.is_empty() and self.validate_max_graphs(max_graphs):
            # logger.debug(f'Current elements: {PRIORITY_QUEUE.heap}')
            element = self.PRIORITY_QUEUE.pop()
            self.queue_size_sequence.append(len(self.PRIORITY_QUEUE.heap))

            # logger.debug(f'Available triads: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads))}')

            if len(element.border) <= 3:
                t_star_graph = update_grid(element, deepcopy(self.BASE_GRAPH))
                self.TOTAL_GRAPHS.append(t_star_graph)
                self.TOTAL_GRAPHS_HISTORY.append(element.border_target_history)
                continue

            selected_triad: Star_Triad_Type = [
                element.border[(element.border_target_index - 1) % len(element.border)],
                element.border[element.border_target_index],
                element.border[(element.border_target_index + 1) % len(element.border)]
            ]
            # logger.debug(f'Selected triad: {[code_to_coordinate[v] for v in selected_triad]}')

            element.border_target_history.append(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])

            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value])
            element.graph[selected_triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]].append(selected_triad[INDEX_ACCESS_TRIAD.VERTEX_1.value])
            
            element.border.remove(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])

            # logger.debug(f'Result: {list(map(lambda triad: list(map(lambda v: code_to_coordinate[v], triad)), element.triads))}')

            for border_target_index in range(len(element.border)):
                evaluation_triad: Star_Triad_Type = [
                    element.border[(border_target_index - 1) % len(element.border)],
                    element.border[border_target_index],
                    element.border[(border_target_index + 1) % len(element.border)]
                ]

                if not verify_not_adjacent(evaluation_triad, element.graph, self.BASE_GRAPH.n):
                    continue

                self.PRIORITY_QUEUE.push(Graph_Priority_Queue.Graph_Priority_Queue_Element(
                    graph=deepcopy(element.graph),
                    border=deepcopy(element.border),
                    border_target_history=deepcopy(element.border_target_history),
                    border_target_index=border_target_index
                ))
        
        self.queue_size_sequence.append(len(self.PRIORITY_QUEUE.heap))

    def define_max_degree_graphs(self):

        GRID: T_Grid_Graph = deepcopy(self.BASE_GRAPH)

        new_edges: list[EdgeType.Coordinate] = []
        if self.BASE_GRAPH.n == 2:
            new_edges = [
                ((0,0), (0,2)),
                ((0,0), (2,0)),
                ((0,2), (2,0)),
            ]
        elif self.BASE_GRAPH.n == 3:
            new_edges = [
                ((0,3), (0,1)),
                ((1,2), (3,0)),
                ((1,2), (2,0)),
                ((1,2), (1,0)),
                ((1,2), (0,1)),
                ((1,2), (0,0)),
            ]
        elif self.BASE_GRAPH.n >= 4:
            if self.BASE_GRAPH.n % 2 == 0:
                origin_connections_coordinate = (self.BASE_GRAPH.n//2, self.BASE_GRAPH.n//2)
                neighbor_omit_coordinates = [
                    (origin_connections_coordinate[0] + 1 , origin_connections_coordinate[1] - 1),
                    (origin_connections_coordinate[0] - 1 , origin_connections_coordinate[1] + 1)
                ]
            else:
                origin_connections_coordinate = (self.BASE_GRAPH.n//2+1, self.BASE_GRAPH.n//2)
                neighbor_omit_coordinates = [
                    (origin_connections_coordinate[0] + 1 , origin_connections_coordinate[1] - 1),
                    (origin_connections_coordinate[0] - 1 , origin_connections_coordinate[1] + 1)
                ]

            border_vertices_coordinates: list[tuple[int, int]] = list(self.BASE_GRAPH.details.coordinate.border)
            border_vertices_coordinates.remove(origin_connections_coordinate)
            border_vertices_coordinates.remove(neighbor_omit_coordinates[0])
            border_vertices_coordinates.remove(neighbor_omit_coordinates[1])

            new_edges = [(origin_connections_coordinate, v) for v in border_vertices_coordinates]

        GRID.add_edges(new_edges)
        self.TOTAL_GRAPHS.append(GRID)
        
    def define_graph(self, max_graphs: int = -1, resultant_graphs: RESULTANT_GRAPHS = RESULTANT_GRAPHS.FULL_SET):
        self.BASE_GRAPH.define_graph()
        if resultant_graphs == RESULTANT_GRAPHS.FULL_SET:
            self.define_full_graphs(max_graphs)
        elif resultant_graphs == RESULTANT_GRAPHS.MAX_DEGREE:
            self.define_max_degree_graphs()

        