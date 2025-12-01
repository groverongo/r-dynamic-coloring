"""Graph theory analysis tools."""

from typing import Dict, List, Any, Optional
import networkx as nx


def compute_basic_properties(graph: nx.Graph) -> Dict[str, Any]:
    """Compute basic graph properties.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary of graph properties
    """
    return {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "is_connected": nx.is_connected(graph),
        "num_components": nx.number_connected_components(graph),
        "density": nx.density(graph),
        "is_tree": nx.is_tree(graph),
        "is_bipartite": nx.is_bipartite(graph),
    }


def compute_degree_info(graph: nx.Graph) -> Dict[str, Any]:
    """Compute degree-related information.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary with degree statistics and distribution
    """
    degrees = dict(graph.degree())
    degree_values = list(degrees.values())
    
    return {
        "degree_sequence": degrees,
        "min_degree": min(degree_values) if degree_values else 0,
        "max_degree": max(degree_values) if degree_values else 0,
        "avg_degree": sum(degree_values) / len(degree_values) if degree_values else 0,
        "is_regular": len(set(degree_values)) == 1,
    }


def compute_centrality(graph: nx.Graph) -> Dict[str, Dict[str, float]]:
    """Compute various centrality measures.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary of centrality measures
    """
    result = {}
    
    try:
        result["degree_centrality"] = nx.degree_centrality(graph)
    except Exception as e:
        result["degree_centrality_error"] = str(e)
    
    try:
        result["betweenness_centrality"] = nx.betweenness_centrality(graph)
    except Exception as e:
        result["betweenness_centrality_error"] = str(e)
    
    try:
        result["closeness_centrality"] = nx.closeness_centrality(graph)
    except Exception as e:
        result["closeness_centrality_error"] = str(e)
    
    try:
        result["eigenvector_centrality"] = nx.eigenvector_centrality(graph, max_iter=100)
    except Exception as e:
        result["eigenvector_centrality_error"] = str(e)
    
    return result


def find_shortest_path(graph: nx.Graph, source: str, target: str) -> Optional[List[str]]:
    """Find the shortest path between two nodes.
    
    Args:
        graph: NetworkX graph
        source: Source node ID
        target: Target node ID
        
    Returns:
        List of node IDs in the path, or None if no path exists
    """
    try:
        path = nx.shortest_path(graph, source=source, target=target)
        return [str(node) for node in path]
    except nx.NetworkXNoPath:
        return None


def compute_all_shortest_paths(graph: nx.Graph, source: str, target: str) -> List[List[str]]:
    """Find all shortest paths between two nodes.
    
    Args:
        graph: NetworkX graph
        source: Source node ID
        target: Target node ID
        
    Returns:
        List of paths, where each path is a list of node IDs
    """
    try:
        paths = nx.all_shortest_paths(graph, source=source, target=target)
        return [[str(node) for node in path] for path in paths]
    except nx.NetworkXNoPath:
        return []


def estimate_chromatic_number(graph: nx.Graph) -> Dict[str, Any]:
    """Estimate the chromatic number of a graph.
    
    Uses greedy coloring and provides bounds.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary with chromatic number estimates and bounds
    """
    # Greedy coloring
    greedy_coloring = nx.greedy_color(graph, strategy="largest_first")
    num_colors = len(set(greedy_coloring.values()))
    
    # Lower bound: maximum clique size
    try:
        # For small graphs, find maximum clique
        if graph.number_of_nodes() <= 50:
            max_clique = len(nx.max_weight_clique(graph, weight=None)[0])
        else:
            max_clique = "Not computed (graph too large)"
    except Exception:
        max_clique = "Unable to compute"
    
    # Upper bound: max degree + 1 (Brooks' theorem)
    max_degree = max(dict(graph.degree()).values()) if graph.number_of_nodes() > 0 else 0
    brooks_bound = max_degree + 1
    
    return {
        "greedy_coloring": greedy_coloring,
        "greedy_num_colors": num_colors,
        "lower_bound_clique": max_clique,
        "upper_bound_brooks": brooks_bound,
        "estimated_chromatic_number": num_colors,
    }


def find_cliques(graph: nx.Graph, min_size: int = 3) -> List[List[str]]:
    """Find all cliques of at least a given size.
    
    Args:
        graph: NetworkX graph
        min_size: Minimum clique size
        
    Returns:
        List of cliques, where each clique is a list of node IDs
    """
    cliques = list(nx.find_cliques(graph))
    # Filter by size and convert to strings
    return [[str(node) for node in clique] for clique in cliques if len(clique) >= min_size]


def analyze_connectivity(graph: nx.Graph) -> Dict[str, Any]:
    """Analyze graph connectivity properties.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary with connectivity information
    """
    result = {
        "is_connected": nx.is_connected(graph),
        "num_connected_components": nx.number_connected_components(graph),
    }
    
    if not result["is_connected"]:
        components = list(nx.connected_components(graph))
        result["component_sizes"] = [len(comp) for comp in components]
        result["largest_component_size"] = max(result["component_sizes"])
    
    # Node and edge connectivity
    if nx.is_connected(graph):
        result["node_connectivity"] = nx.node_connectivity(graph)
        result["edge_connectivity"] = nx.edge_connectivity(graph)
    
    return result


def detect_cycles(graph: nx.Graph) -> Dict[str, Any]:
    """Detect cycles in the graph.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary with cycle information
    """
    try:
        cycles = nx.cycle_basis(graph)
        return {
            "has_cycles": len(cycles) > 0,
            "num_cycles": len(cycles),
            "cycles": [[str(node) for node in cycle] for cycle in cycles[:10]],  # Limit to 10
            "truncated": len(cycles) > 10,
        }
    except Exception as e:
        return {"error": str(e)}


def compute_comprehensive_analysis(graph: nx.Graph) -> Dict[str, Any]:
    """Run a comprehensive analysis on the graph.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        Dictionary containing all analysis results
    """
    return {
        "basic_properties": compute_basic_properties(graph),
        "degree_info": compute_degree_info(graph),
        "centrality": compute_centrality(graph),
        "chromatic_info": estimate_chromatic_number(graph),
        "connectivity": analyze_connectivity(graph),
        "cycles": detect_cycles(graph),
    }
