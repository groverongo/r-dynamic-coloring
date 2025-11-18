from eulerian.graph import SampleGraph

def coloring_algorithm(graph: SampleGraph):
    vertex_neighbor_colors = {vertex: set() for vertex in graph.get_vertices()}
    vertex_uncolored_neighbors = {vertex: graph.degree(vertex) for vertex in graph.get_vertices()}
    vertex_coloring = {vertex: None for vertex in graph.get_vertices()}

    vertices = graph.get_vertices().copy()
    for vertex in vertices:
        neighbors = graph.get_neighbors(vertex)

        color: int = 0
        for color in range(1, 6+1):
            if color in vertex_neighbor_colors[vertex]:
                continue

                                          
            
            break

        vertex_coloring[vertex] = color
        vertex_uncolored_neighbors[vertex] -= 1
        for neighbor in neighbors:
            vertex_neighbor_colors[neighbor].add(color)
            

        