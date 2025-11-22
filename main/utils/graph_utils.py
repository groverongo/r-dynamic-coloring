from typing import Dict, List

def adjacency_matrix_to_adjacency_list(graph: List[List[int]]) -> Dict[int, List[int]]:
    """Convert an adjacency matrix to an adjacency list.
    
    Args:
        graph: Adjacency matrix as a 2D list
        
    Returns:
        Adjacency list as a dictionary
    """
    return {i: [j for j in range(len(graph)) if graph[i][j] == 1] for i in range(len(graph))}
