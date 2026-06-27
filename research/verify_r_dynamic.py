def is_proper_coloring(graph, coloring):
    """
    Check if a coloring is proper (adjacent vertices have different colors).

    Args:
        graph: Dictionary representing adjacency list
        coloring: Dictionary mapping vertices to colors

    Returns:
        Tuple (is_proper, violations) where violations is a list of edges
        with the same color
    """
    violations = []
    for vertex in graph:
        vertex_color = coloring.get(vertex)
        if vertex_color is None:
            return False, [(vertex, "No color assigned")]

        for neighbor in graph[vertex]:
            neighbor_color = coloring.get(neighbor)
            if neighbor_color is None:
                return False, [(neighbor, "No color assigned")]

            if vertex_color == neighbor_color:
                if vertex < neighbor:
                    violations.append((vertex, neighbor, vertex_color))

    return len(violations) == 0, violations


def is_r_dynamic(graph, coloring, r):
    """
    Check if a coloring is r-dynamic.

    For each vertex v, the neighborhood of v must have at least
    min(r, degree(v)) different colors.

    Args:
        graph: Dictionary representing adjacency list
        coloring: Dictionary mapping vertices to colors
        r: The r parameter (integer > 0)

    Returns:
        Tuple (is_dynamic, violations) where violations is a list of vertices
        that violate the r-dynamic property
    """
    if r <= 0:
        raise ValueError("r must be a positive integer")

    violations = []

    for vertex in graph:
        neighbors = graph[vertex]
        degree = len(neighbors)
        required_colors = min(r, degree)

        if required_colors == 0:
            continue

        neighborhood_colors = set()
        for neighbor in neighbors:
            neighborhood_colors.add(coloring[neighbor])

        num_colors = len(neighborhood_colors)

        if num_colors < required_colors:
            violations.append({
                'vertex': vertex,
                'degree': degree,
                'required_colors': required_colors,
                'actual_colors': num_colors,
                'neighborhood_colors': sorted(neighborhood_colors)
            })

    return len(violations) == 0, violations


def verify_r_dynamic_coloring(graph, coloring, r):
    """
    Verify if a coloring is both proper and r-dynamic.

    Args:
        graph: Dictionary representing adjacency list
        coloring: Dictionary mapping vertices to colors
        r: The r parameter

    Returns:
        Dictionary with detailed verification results
    """
    is_proper, proper_violations = is_proper_coloring(graph, coloring)
    is_dynamic, dynamic_violations = is_r_dynamic(graph, coloring, r)

    return {
        'is_proper': is_proper,
        'is_r_dynamic': is_dynamic,
        'is_valid': is_proper and is_dynamic,
        'proper_violations': proper_violations,
        'dynamic_violations': dynamic_violations,
        'r': r
    }


def print_verification_results(results):
    """Pretty print verification results."""
    print(f"\n{'='*60}")
    print(f"r-Dynamic Coloring Verification (r={results['r']})")
    print(f"{'='*60}")

    print(f"\nProper Coloring: {'✓ YES' if results['is_proper'] else '✗ NO'}")
    if not results['is_proper']:
        print(f"  Violations found: {len(results['proper_violations'])}")
        for violation in results['proper_violations'][:5]:
            print(f"    {violation}")

    print(f"\nr-Dynamic Coloring: {'✓ YES' if results['is_r_dynamic'] else '✗ NO'}")
    if not results['is_r_dynamic']:
        print(f"  Violations found: {len(results['dynamic_violations'])}")
        for violation in results['dynamic_violations'][:5]:
            print(f"    Vertex {violation['vertex']}: degree={violation['degree']}, "
                  f"required={violation['required_colors']}, "
                  f"actual={violation['actual_colors']}")

    print(f"\nOverall Valid: {'✓ YES' if results['is_valid'] else '✗ NO'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Example usage with a star graph (center vertex 0)
    graph = {
        0: {1, 2, 3},
        1: {0},
        2: {0},
        3: {0}
    }

    # Example 1: Valid r-dynamic coloring for r=2
    print("Example 1: Valid r-dynamic coloring (r=2)")
    coloring1 = {0: 'red', 1: 'blue', 2: 'green', 3: 'yellow'}
    results1 = verify_r_dynamic_coloring(graph, coloring1, r=2)
    print_verification_results(results1)

    # Example 2: Invalid coloring (not proper - adjacent vertices same color)
    print("Example 2: Invalid coloring (adjacent vertices same color)")
    coloring2 = {0: 'red', 1: 'red', 2: 'blue', 3: 'green'}
    results2 = verify_r_dynamic_coloring(graph, coloring2, r=2)
    print_verification_results(results2)

    # Example 3: Proper but not 2-dynamic
    print("Example 3: Proper coloring but not 2-dynamic")
    coloring3 = {0: 'red', 1: 'blue', 2: 'blue', 3: 'blue'}
    results3 = verify_r_dynamic_coloring(graph, coloring3, r=2)
    print_verification_results(results3)
