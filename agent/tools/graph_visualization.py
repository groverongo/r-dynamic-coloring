"""Graph visualization tool using NetworkX and Matplotlib."""

from typing import Dict, List, Optional, Literal
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime
import io

from config import config


def generate_graph_visualization(
    graph: nx.Graph,
    layout: Literal["spring", "circular", "kamada_kawai", "planar", "shell", "spectral"] = "spring",
    node_coloring: Optional[Dict[str, str]] = None,
    edge_coloring: Optional[Dict[tuple[str, str], str]] = None,
    highlight_nodes: Optional[List[str]] = None,
    highlight_edges: Optional[List[tuple[str, str]]] = None,
    title: Optional[str] = None,
    figsize: tuple[int, int] = (12, 10),
    node_size: int = 500,
    save_path: Optional[Path] = None,
) -> Path:
    """Generate a visualization of a NetworkX graph.
    
    Args:
        graph: NetworkX graph to visualize
        layout: Layout algorithm to use
        node_coloring: Dictionary mapping node IDs to colors
        edge_coloring: Dictionary mapping edge tuples to colors
        highlight_nodes: List of nodes to highlight with thicker borders
        highlight_edges: List of edges to highlight with thicker lines
        title: Title for the graph visualization
        figsize: Figure size as (width, height) in inches
        node_size: Size of nodes
        save_path: Optional path to save the image. If None, auto-generates path.
        
    Returns:
        Path to the saved visualization image
    """
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Select layout
    layout_functions = {
        "spring": nx.spring_layout,
        "circular": nx.circular_layout,
        "kamada_kawai": nx.kamada_kawai_layout,
        "planar": nx.planar_layout,
        "shell": nx.shell_layout,
        "spectral": nx.spectral_layout,
    }
    
    try:
        pos = layout_functions[layout](graph)
    except Exception as e:
        # Fallback to spring layout
        print(f"Layout {layout} failed: {e}. Using spring layout.")
        pos = nx.spring_layout(graph)
    
    # Prepare node colors
    if node_coloring:
        node_colors = [node_coloring.get(str(node), "#1f78b4") for node in graph.nodes()]
    else:
        node_colors = "#1f78b4"
    
    # Prepare edge colors
    if edge_coloring:
        edge_colors = []
        for edge in graph.edges():
            # Try both orderings of the edge
            color = edge_coloring.get(edge) or edge_coloring.get((edge[1], edge[0]))
            edge_colors.append(color if color else "#888888")
    else:
        edge_colors = "#888888"
    
    # Prepare node borders for highlights
    node_edge_colors = []
    node_linewidths = []
    for node in graph.nodes():
        if highlight_nodes and str(node) in highlight_nodes:
            node_edge_colors.append("#ff0000")
            node_linewidths.append(3.0)
        else:
            node_edge_colors.append("#000000")
            node_linewidths.append(1.0)
    
    # Prepare edge widths for highlights
    edge_widths = []
    for edge in graph.edges():
        if highlight_edges and (edge in highlight_edges or (edge[1], edge[0]) in highlight_edges):
            edge_widths.append(3.0)
        else:
            edge_widths.append(1.0)
    
    # Draw the graph
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color=edge_colors,
        width=edge_widths,
        alpha=0.6,
        ax=ax
    )
    
    nx.draw_networkx_nodes(
        graph, pos,
        node_color=node_colors,
        node_size=node_size,
        edgecolors=node_edge_colors,
        linewidths=node_linewidths,
        ax=ax
    )
    
    nx.draw_networkx_labels(
        graph, pos,
        font_size=10,
        font_weight="bold",
        ax=ax
    )
    
    # Set title
    if title:
        ax.set_title(title, fontsize=16, fontweight="bold")
    else:
        ax.set_title(
            f"Graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges",
            fontsize=14
        )
    
    ax.axis("off")
    plt.tight_layout()
    
    # Save the visualization
    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = config.VISUALIZATION_DIR / f"graph_{timestamp}.png"
    
    # Ensure parent directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    
    return save_path


def get_available_layouts() -> List[str]:
    """Get list of available graph layout algorithms.
    
    Returns:
        List of layout names
    """
    return ["spring", "circular", "kamada_kawai", "planar", "shell", "spectral"]


def validate_coloring(graph: nx.Graph, coloring: Dict[str, str]) -> tuple[bool, Optional[str]]:
    """Validate a node coloring for a graph.
    
    Checks if the coloring is a valid assignment where no two adjacent nodes
    have the same color.
    
    Args:
        graph: NetworkX graph
        coloring: Dictionary mapping node IDs to colors
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check all nodes are colored
    for node in graph.nodes():
        if str(node) not in coloring:
            return False, f"Node {node} is not colored"
    
    # Check adjacent nodes have different colors
    for edge in graph.edges():
        node1, node2 = str(edge[0]), str(edge[1])
        if coloring[node1] == coloring[node2]:
            return False, f"Adjacent nodes {node1} and {node2} have the same color: {coloring[node1]}"
    
    return True, None
