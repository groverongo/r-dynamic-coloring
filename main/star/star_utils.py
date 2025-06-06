from typing import Dict, List, Union
from graph.graph_coloring import T_Grid_Graph
from .star_types import INDEX_ACCESS_TRIAD, Star_Triad_Type
from .star_details import Graph_Priority_Queue
from graph.graph_types import VertexType

def verify_not_corner(triad: Star_Triad_Type, to_coordinate: Dict[VertexType.Code, VertexType.Coordinate], n: int):
    vertex_1, _, vertex_2 = triad
    vertex_1_coordinate = to_coordinate[vertex_1]
    vertex_2_coordinate = to_coordinate[vertex_2]
    
    if (vertex_1_coordinate == (0,1) and vertex_2_coordinate == (1,0)) or (vertex_1_coordinate == (1,0) and vertex_2_coordinate == (0,1)):
        return False

    if (vertex_1_coordinate == (n-1, 0) and vertex_2_coordinate == (n-1, 1)) or (vertex_1_coordinate == (n-1, 1) and vertex_2_coordinate == (n-1, 0)):
        return False

    if (vertex_1_coordinate == (0, n-1) and vertex_2_coordinate == (1, n-1)) or (vertex_1_coordinate == (1, n-1) and vertex_2_coordinate == (0, n-1)):
        return False

    return True

def update_grid(element: Graph_Priority_Queue.Graph_Priority_Queue_Element, graph: T_Grid_Graph):
    graph.details.code.adjacency_list = element.graph
    graph.details.code.border = list(element.border)
    graph.details.code.edges = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in element.graph for final_vertex in element.graph[initial_vertex]]))
    
    graph.details.coordinate.adjacency_list = {graph.details.code.to_other[initial_vertex]: [graph.details.code.to_other[final_vertex] for final_vertex in element.graph[initial_vertex]] for initial_vertex in element.graph}
    graph.details.coordinate.border = [graph.details.code.to_other[border_vertex] for border_vertex in graph.details.code.border]
    graph.details.coordinate.edges = [(graph.details.code.to_other[edge[0]], graph.details.code.to_other[edge[1]]) for edge in graph.details.code.edges]

    graph.details.misc.degree = {vertex: len(graph.details.code.adjacency_list) for vertex in graph.details.code.adjacency_list}
    
    return graph

def middle_vertex_presence_filter(triad: Star_Triad_Type, selected_triad: Star_Triad_Type):
    try:
        return triad.index(selected_triad[INDEX_ACCESS_TRIAD.MIDDLE.value])
    except ValueError:
        return -1