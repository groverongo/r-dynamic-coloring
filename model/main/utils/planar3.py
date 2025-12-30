from typing import Dict, List, Union
import networkx as nx
import matplotlib.pyplot as plt

def generate_planar_3_tree(n: int, output_format: str = 'list') -> Union[Dict[int, List[int]], List[List[int]]]:
    """
    Generates an iterative planar 3-tree graph.
    
    The graph starts as a K3 (a triangle). In each iteration, a new vertex 
    is added inside every face (including the outer face) and connected 
    to the three vertices forming that face.
    
    Efficiency Analysis:
    -------------------
    The best output format for this graph is the **Adjacency List**.
    
    1. **Sparsity**: Planar graphs are sparse by nature (edges E <= 3V - 6). 
       An adjacency list stores only existing edges, making it much more 
       memory-efficient than an adjacency matrix, which stores V^2 entries.
    2. **Exponential Growth**: The number of vertices grows exponentially 
       with the number of iterations (V = 3^n + 2). 
       - At n=0: V=3
       - At n=1: V=5
       - At n=5: V=245
       - At n=10: V=59,051
       For n=10, a dense adjacency matrix would consume several gigabytes of RAM,
       while an adjacency list remains lightweight.
    
    Args:
        n (int): The number of iterations to perform. 
        output_format (str): 'list' for an adjacency list (dict of lists) 
                             or 'matrix' for an adjacency matrix (list of lists).
                             
    Returns:
        Union[Dict[int, List[int]], List[List[int]]]: The generated graph.
    """
    
    # Start with K3
    # Vertices: 0, 1, 2
    # Adjacency list representation
    adj = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    
    # Faces are represented by triples of vertices in cyclic order.
    # Initially, K3 has two faces (the "inside" and "outside").
    faces = [(0, 1, 2)]
    # faces = [(0, 1, 2), (0, 2, 1)]
    
    next_vertex = 3
    
    # Perform n iterations
    for _ in range(n):
        new_faces = []
        for u, v, w in faces:
            # Create a new vertex in this face
            z = next_vertex
            next_vertex += 1
            
            # Connect new vertex z to the three vertices of the face
            adj[z] = [u, v, w]
            adj[u].append(z)
            adj[v].append(z)
            adj[w].append(z)
            
            # This face (u, v, w) is replaced by three new triangular faces:
            # (u, v, z), (v, w, z), (w, u, z)
            new_faces.append((u, v, z))
            new_faces.append((v, w, z))
            new_faces.append((w, u, z))
            
        faces = new_faces
        
    if output_format == 'matrix':
        num_v = next_vertex
        # Initialize matrix with 0s
        matrix = [[0 for _ in range(num_v)] for _ in range(num_v)]
        # Fill the matrix based on the adjacency list
        for u, neighbors in adj.items():
            for v in neighbors:
                matrix[u][v] = 1
        return matrix
    
    return adj

def visualize_planar_3_tree(graph_data: Union[Dict[int, List[int]], List[List[int]]]):
    """
    Visualizes the planar 3-tree using NetworkX and Matplotlib.
    
    Args:
        graph_data: Adjacency list (dict) or Adjacency matrix (list of lists).
    """
    if isinstance(graph_data, dict):
        G = nx.Graph(graph_data)
    else:
        G = nx.Graph()
        num_v = len(graph_data)
        for i in range(num_v):
            for j in range(i + 1, num_v):
                if graph_data[i][j] == 1:
                    G.add_edge(i, j)
    
    plt.figure(figsize=(10, 8))
    
    # Try planar layout if graph is small, otherwise fall back to spring layout
    try:
        if len(G.nodes) < 100:
            pos = nx.planar_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)
    except nx.NetworkXException:
        # Sometimes planar_layout fails even if the graph is planar (e.g. implementation limits)
        pos = nx.spring_layout(G, seed=42)
        
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=500, edge_color='gray', font_size=10, font_weight='bold')
    
    plt.title(f"Planar 3-tree (|V|={len(G.nodes)}, |E|={len(G.edges)})")
    
    # In many environments, the user might want the file saved or shown
    # Saving as a temporary file is often safer for automated environments
    output_path = "planar3_tree_visualization.png"
    print(f"Visualization saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    # Example usage:
    # n=1 should produce a triangular bipyramid (5 vertices)
    graph = generate_planar_3_tree(4, output_format='list')
    print(f"Planar 3-tree (n=4) Adjacency List: {graph}")
    
    # Visualize the n=2 case (11 vertices)
    print("Generating visualization for n=2...")
    graph_n2 = generate_planar_3_tree(4, output_format='list')
    visualize_planar_3_tree(graph_n2)
    
    # n=0 should produce K3
    k3 = generate_planar_3_tree(0, output_format='matrix')
    print(f"K3 Adjacency Matrix: {k3}")
