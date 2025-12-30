# Your first line of Python code
from typing import List
import numpy as np
import sys

def create_antiprism_adjacency_matrix(n):
    """
    Generates the adjacency matrix for an n-antiprism graph.
    The graph is isomorphic to the circulant graph Ci_(2n)(1,2).
    
    Args:
        n (int): Defines the antiprism (must be even, based on user query).
        
    Returns:
        numpy.ndarray: The 2n x 2n adjacency matrix.
    """
    
    # # 1. Validate Input (based on user query constraint)
    # if n % 2 != 0:
    #     print("Error: The input 'n' must be an even number as requested.", file=sys.stderr)
    #     return None
        
    # N is the total number of vertices (2n) [1]
    N = 2 * n
    
    # Initialize the N x N adjacency matrix with zeros
    A = np.zeros((N, N), dtype=int)
    
    # The circulant graph Ci_(N)(1,2) connects each vertex i to:
    # i ± 1 (modulo N) and i ± 2 (modulo N).
    connection_set = {1, 2}
    
    # 2. Populate the Matrix
    for i in range(N):
        for s in connection_set:
            # Connection i + s (forward connection)
            j_plus = (i + s) % N
            A[i, j_plus] = 1
            
            # Connection i - s (backward connection)
            # We add N before taking modulo to ensure positive results for negative indices
            j_minus = (i - s + N) % N
            A[i, j_minus] = 1
            
    # The matrix is now complete, defined by the Ci_(2n)(1,2) structure [1]
    return A.tolist()

def create_circulant_adjacency_matrix(n: int, *connections: int):
    A = np.zeros((n, n), dtype=int)

    connection_set = set(filter(lambda x: x <= n//2 and x > 0, connections))

    for i in range(n):
        for s in connection_set:
            j_plus = (i + s) % n
            A[i, j_plus] = 1
            
            j_minus = (i - s + n) % n
            A[i, j_minus] = 1
    
    return A.tolist()