from typing import List, Union
from graph.graph_coloring import T_Grid_Graph
from .star_types import INDEX_ACCESS_TRIAD, Star_Triad_Type
from .star_details import Graph_Priority_Queue

def update_grid(element: Graph_Priority_Queue.Graph_Priority_Queue_Element, graph: T_Grid_Graph):
    graph.details.code.adjacency_list = element.graph
    graph.details.code.border = element.border
    graph.details.code.triad_candidates = element.triads
    graph.details.code.edges = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in element.graph for final_vertex in element.graph[initial_vertex]]))
    
    graph.details.coordinate.adjacency_list = {graph.details.code.to_other[initial_vertex]: [graph.details.code.to_other[final_vertex] for final_vertex in element.graph[initial_vertex]] for initial_vertex in element.graph}
    graph.details.coordinate.border = [graph.details.code.to_other[border_vertex] for border_vertex in element.border]
    graph.details.coordinate.triad_candidates = [(graph.details.code.to_other[triad[0]], graph.details.code.to_other[triad[1]], graph.details.code.to_other[triad[2]]) for triad in element.triads]
    graph.details.coordinate.edges = [(graph.details.code.to_other[edge[0]], graph.details.code.to_other[edge[1]]) for edge in graph.details.code.edges]
    
    return graph

def obtain_candidate_vertex(selected_triad: Star_Triad_Type, triad_candidates: List[Star_Triad_Type], terminal_vertex: Union[INDEX_ACCESS_TRIAD.VERTEX_1, INDEX_ACCESS_TRIAD.VERTEX_2]):
    for triad in triad_candidates:
        if selected_triad[terminal_vertex.value] == triad[INDEX_ACCESS_TRIAD.MIDDLE.value]:
            if selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value] == triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]:
                return triad[INDEX_ACCESS_TRIAD.VERTEX_2.value]
            else:
                return triad[INDEX_ACCESS_TRIAD.VERTEX_1.value]
        else:
            return triad[INDEX_ACCESS_TRIAD.MIDDLE.value]

def middle_vertex_presence_filter(triad: Star_Triad_Type):
    try:
        return triad.index(triad[INDEX_ACCESS_TRIAD.MIDDLE.value])
    except ValueError:
        return -1