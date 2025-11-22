from typing import Dict, List, Tuple, Optional
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import numpy as np

from ..coloring.r_dynamic import linear_programming_model
from ..schemas.requests import AntiprismBatchRequest
from ..utils.graph_utils import adjacency_matrix_to_adjacency_list
from ..utils.antiprism import create_antiprism_adjacency_matrix

class ColoringService:
    @staticmethod
    def color_graph(adjacency_list: Dict[int, List[int]], method: str, k: int, r: int) -> Dict[int, int]:
        """Color a graph using the specified method.
        
        Args:
            adjacency_list: Graph represented as an adjacency list
            method: Coloring method to use
            k: Number of colors
            r: Dynamic coloring order
            
        Returns:
            Dictionary mapping vertices to their assigned colors
        """
        solution = linear_programming_model(
            adjacency_list=adjacency_list,
            model_name=method,
            k=k,
            r=r
        )
        
        color_assignment = {v: [x_vc.varValue for x_vc in x_v].index(1) 
                          for v, x_v in enumerate(solution.x)}
        
        logger.info(f'Solution: {color_assignment}')
        return color_assignment
    
    @staticmethod
    def process_single_case(r: int, n: int, method: str, k: int) -> tuple[int, int, Optional[Dict[int, int]], Optional[str]]:
        """Process a single (r, n) case for antiprism coloring.
        
        Args:
            r: Dynamic coloring order
            n: Number of vertices in the antiprism graph
            method: Coloring method to use
            k: Number of colors
            
        Returns:
            Tuple containing (r, n, color_assignment, error)
        """
        logger.info(f'Processing: r={r}, n={n}')
        try:
            adjacency_matrix = create_antiprism_adjacency_matrix(n)
            adjacency_list = adjacency_matrix_to_adjacency_list(adjacency_matrix)
            color_assignment = ColoringService.color_graph(adjacency_list, method, k, r)
            logger.info(f'Solution for r={r}, n={n}: {color_assignment}')
            return r, n, color_assignment, None
        except Exception as e:
            logger.error(f'Error: {e} on r={r}, n={n}')
            return r, n, None, str(e)
    
    @staticmethod
    def process_antiprism_batch(request: AntiprismBatchRequest) -> Dict[int, Dict[int, Dict[int, int]]]:
        """Process a batch of antiprism coloring requests.
        
        Args:
            request: Batch request containing parameters for multiple colorings
            
        Returns:
            Nested dictionary of color assignments: {r: {n: color_assignment}}
        """
        logger.info(f'Antiprism Batch Request: {request}')
        solutions_object = {}
        
        r_values = range(request.r_range[0], request.r_range[1] + 1)
        n_values = range(request.n_range[0], request.n_range[1] + 1)
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for r in r_values:
                for n in n_values:
                    futures.append(executor.submit(
                        ColoringService.process_single_case,
                        r=r,
                        n=n,
                        method=request.method,
                        k=request.k
                    ))
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(futures):
                r, n, result, error = future.result()
                if error is None:
                    solutions_object.setdefault(r, {})[n] = result
                else:
                    logger.error(f"Failed to process r={r}, n={n}: {error}")
        
        return solutions_object
