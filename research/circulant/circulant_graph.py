def generate_circulant_graph(n):
    """
    Generate a circulant graph C(n; 1, 3).

    Each vertex i is connected to:
    - (i+1 mod n) and (i-1 mod n) from the 1 parameter
    - (i+3 mod n) and (i-3 mod n) from the 3 parameter

    Args:
        n: Number of vertices (must be > 0)

    Returns:
        A dictionary representing the adjacency list where keys are vertices
        and values are sets of adjacent vertices
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    adjacency_list = {i: set() for i in range(n)}

    for i in range(n):
        # Add edges for parameter 1 (immediate neighbors in the cycle)
        adjacency_list[i].add((i + 1) % n)
        adjacency_list[i].add((i - 1) % n)

        # Add edges for parameter 3
        adjacency_list[i].add((i + 3) % n)
        adjacency_list[i].add((i - 3) % n)

    return adjacency_list


def print_adjacency_list(adj_list):
    """Pretty print the adjacency list."""
    for vertex in sorted(adj_list.keys()):
        neighbors = sorted(adj_list[vertex])
        print(f"{vertex}: {neighbors}")


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8

    graph = generate_circulant_graph(n)
    print(f"Circulant Graph C({n}; 1, 3):")
    print_adjacency_list(graph)
