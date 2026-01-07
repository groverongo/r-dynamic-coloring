from typing import List, Dict
import networkx as nx
import matplotlib.pyplot as plt
import io

def plot_graph_to_bytes(adjacency_list: Dict[int, List[int]], coloring: Dict[int, int]) -> bytes:
    """
    Plots a graph with colored vertices based on an adjacency list and coloring dictionary.
    Returns the generated image as bytes (PNG format).
    
    Args:
        adjacency_list: A dictionary where keys are node IDs and values are lists of neighbor IDs.
        coloring: A dictionary mapping node IDs to their assigned color (integer).
        
    Returns:
        bytes: The PNG image data.
    """
    # Initialize the graph
    G = nx.Graph()
    
    # Add all nodes first to ensure they exist even if they have no neighbors
    G.add_nodes_from(adjacency_list.keys())
    
    # Add edges
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Create the figure with a high-definition setting
    plt.figure(figsize=(12, 10), dpi=100, facecolor='none')
    
    # Calculate a layout that looks balanced
    pos = nx.spring_layout(G, k=0.2, iterations=60)
    
    # Get the sequence of nodes and their corresponding colors
    node_list = list(G.nodes())
    colors = [coloring.get(node, 0) for node in node_list]
    
    # Draw the edges with subtle styling
    nx.draw_networkx_edges(
        G, pos, 
        # alpha=0.4, 
        edge_color="#A0A0A0", 
        width=1.5
    )
    
    # Draw the nodes with a premium qualitative colormap
    # 'Set2', 'Set3', or 'Paired' are excellent for discrete graph colorings
    print(colors)
    nx.draw_networkx_nodes(
        G, pos, 
        nodelist=node_list,
        node_color=colors,
        cmap=plt.cm.get_cmap('Set3'),
        node_size=800,
        edgecolors='#2C3E50',
        linewidths=2.0
    )
    
    # Add labels with a clean, centered font
    nx.draw_networkx_labels(
        G, pos, 
        font_size=11, 
        font_family="sans-serif", 
        font_weight="bold",
        font_color="#2C3E50"
    )

    # Final touches: remove axis, set tight layout
    plt.axis('off')
    plt.tight_layout(pad=0)

    # Export to a bytes buffer
    buf = io.BytesIO()
    plt.show()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close()
    
    buf.seek(0)
    image_bytes = buf.getvalue()
    buf.close()
    
    return image_bytes

if __name__ == "__main__":
    
    data = plot_graph_to_bytes(
        {0: [1, 3, 7, 9], 1: [0, 2, 4, 8], 2: [1, 3, 5, 9], 3: [0, 2, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 6, 8], 6: [3, 5, 7, 9], 7: [0, 4, 6, 8], 8: [1, 5, 7, 9], 9: [0, 2, 6, 8]},
        {
        0: 1,
        1: 4,
        2: 3,
        3: 2,
        4: 0,
        5: 1,
        6: 4,
        7: 3,
        8: 2,
        9: 0
    }
    )

    # plot the image
    plt.imshow(data)
    plt.show()