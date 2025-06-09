from typing import Dict, List, Union
from graph.graph_coloring import T_Grid_Graph
from .star_types import INDEX_ACCESS_TRIAD, Star_Triad_Type
from .star_details import Graph_Priority_Queue
from graph.graph_types import VertexType

def verify_not_adjacent(triad: Star_Triad_Type, adjacency_list: Dict[VertexType.Code, List[VertexType.Code]], n: int):
    vertex_1, _, vertex_2 = triad

    # Check that vertex_1 and vertex_2 are not adjacent
    if vertex_2 in adjacency_list[vertex_1]:
        return False

    return True

def update_grid(element: Graph_Priority_Queue.Graph_Priority_Queue_Element, graph: T_Grid_Graph):
    graph.details.code.adjacency_list = element.graph
    graph.details.code.border = list(element.border)
    graph.details.code.edges = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in element.graph for final_vertex in element.graph[initial_vertex]]))
    
    graph.details.coordinate.adjacency_list = {graph.details.code.to_other[initial_vertex]: [graph.details.code.to_other[final_vertex] for final_vertex in element.graph[initial_vertex]] for initial_vertex in element.graph}
    graph.details.coordinate.border = [graph.details.code.to_other[border_vertex] for border_vertex in graph.details.code.border]
    graph.details.coordinate.edges = [(graph.details.code.to_other[edge[0]], graph.details.code.to_other[edge[1]]) for edge in graph.details.code.edges]

    graph.details.misc.degree = {vertex: len(graph.details.code.adjacency_list[vertex]) for vertex in graph.details.code.adjacency_list}
    
    return graph

def middle_vertex_presence_filter(triad: Star_Triad_Type, selected_triad: Star_Triad_Type):
    try:
        return triad.index(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])
    except ValueError:
        return -1