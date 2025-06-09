def has_repeated_edges(adjacency_list: dict[int, list[int]]):
    """
    Check if a graph represented by an adjacency list has any repeated edges.
    In an undirected graph, (u,v) and (v,u) are considered the same edge.
    
    Args:
        adjacency_list (dict): A dictionary where keys are vertices and values are lists of adjacent vertices.
        
    Returns:
        bool: True if there are repeated edges, False otherwise.
    """
    # For each vertex, track which neighbors we've seen
    seen_neighbors = {v: set() for v in adjacency_list}
    
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            # For undirected graphs, we only need to check in one direction
            if vertex > neighbor:
                continue
                
            if neighbor in seen_neighbors[vertex]:
                # Found a duplicate edge
                return True
            seen_neighbors[vertex].add(neighbor)
            
    return False