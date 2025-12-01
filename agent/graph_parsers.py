"""Graph input parsing utilities."""

from typing import Dict, List, Union, Optional
import networkx as nx
from PIL import Image
import io


def parse_adjacency_list(adj_list: Dict[str, List[str]]) -> nx.Graph:
    """Parse an adjacency list into a NetworkX graph.
    
    Args:
        adj_list: Dictionary mapping node IDs to lists of adjacent node IDs
                 Example: {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
    
    Returns:
        NetworkX graph object
        
    Raises:
        ValueError: If the adjacency list is invalid
    """
    if not isinstance(adj_list, dict):
        raise ValueError("Adjacency list must be a dictionary")
    
    G = nx.Graph()
    
    # Add all nodes first
    for node in adj_list.keys():
        G.add_node(str(node))
    
    # Add edges
    for node, neighbors in adj_list.items():
        if not isinstance(neighbors, list):
            raise ValueError(f"Neighbors of node {node} must be a list")
        
        for neighbor in neighbors:
            # Ensure both nodes exist
            if str(neighbor) not in adj_list:
                G.add_node(str(neighbor))
            G.add_edge(str(node), str(neighbor))
    
    return G


def parse_adjacency_matrix(adj_matrix: List[List[Union[int, str]]], 
                          node_labels: Optional[List[str]] = None) -> nx.Graph:
    """Parse an adjacency matrix into a NetworkX graph.
    
    Args:
        adj_matrix: 2D list representing the adjacency matrix
                   Example: [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
        node_labels: Optional list of node labels. If not provided,
                    nodes will be labeled as "0", "1", "2", etc.
    
    Returns:
        NetworkX graph object
        
    Raises:
        ValueError: If the adjacency matrix is invalid
    """
    if not isinstance(adj_matrix, list):
        raise ValueError("Adjacency matrix must be a list")
    
    if not adj_matrix:
        raise ValueError("Adjacency matrix cannot be empty")
    
    # Validate square matrix
    n = len(adj_matrix)
    for i, row in enumerate(adj_matrix):
        if not isinstance(row, list):
            raise ValueError(f"Row {i} must be a list")
        if len(row) != n:
            raise ValueError(f"Adjacency matrix must be square. Row {i} has {len(row)} elements, expected {n}")
    
    # Create node labels
    if node_labels is None:
        node_labels = [str(i) for i in range(n)]
    elif len(node_labels) != n:
        raise ValueError(f"Number of node labels ({len(node_labels)}) must match matrix size ({n})")
    
    # Convert to NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    for label in node_labels:
        G.add_node(str(label))
    
    # Add edges based on adjacency matrix
    for i in range(n):
        for j in range(i, n):  # Only check upper triangle to avoid duplicate edges
            # Convert to int/float for comparison
            try:
                weight = float(adj_matrix[i][j])
                if weight != 0:  # Non-zero means there's an edge
                    G.add_edge(str(node_labels[i]), str(node_labels[j]))
            except (ValueError, TypeError):
                # If conversion fails, treat non-empty string as edge
                if adj_matrix[i][j]:
                    G.add_edge(str(node_labels[i]), str(node_labels[j]))
    
    return G


def parse_graph_image(image_data: Union[bytes, str, Image.Image]) -> tuple[nx.Graph, str]:
    """Parse a graph image using Gemini vision.
    
    This function uses Gemini's vision capabilities to extract graph structure
    from an image and convert it to a NetworkX graph.
    
    Args:
        image_data: Image as bytes, file path, or PIL Image object
    
    Returns:
        Tuple of (NetworkX graph object, description from Gemini)
        
    Raises:
        ValueError: If the image cannot be processed
        
    Note:
        This function requires Gemini API access and will be implemented
        in the tools module with proper error handling.
    """
    # This is a placeholder - actual implementation will use Gemini vision
    # and will be implemented in tools/image_parsing.py
    raise NotImplementedError(
        "Image-based graph parsing requires Gemini vision integration. "
        "This will be implemented in the tools module."
    )


def validate_graph(G: nx.Graph) -> bool:
    """Validate that a NetworkX graph is properly formed.
    
    Args:
        G: NetworkX graph to validate
        
    Returns:
        True if valid, raises exception otherwise
        
    Raises:
        ValueError: If the graph is invalid
    """
    if not isinstance(G, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
        raise ValueError("Not a valid NetworkX graph object")
    
    if G.number_of_nodes() == 0:
        raise ValueError("Graph has no nodes")
    
    return True
