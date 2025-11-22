from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import Dict, List

from ..utils.antiprism import create_antiprism_adjacency_matrix
from ..schemas.requests import ColoringGraphRequest, AntiprismRequest, AntiprismBatchRequest
from ..services.coloring_service import ColoringService
from ..utils.graph_utils import adjacency_matrix_to_adjacency_list

router = APIRouter()

@router.post("/color/graph")
async def assign_colors(request: ColoringGraphRequest) -> Dict[str, Dict[int, int]]:
    """
    Assign colors to a graph using the specified method.
    
    Args:
        request: The coloring request containing graph and parameters
        
    Returns:
        Dictionary mapping vertices to their assigned colors
    """
    try:
        if request.graph_type == 'adjacency_matrix':
            request.graph = adjacency_matrix_to_adjacency_list(request.graph)
            
        color_assignment = ColoringService.color_graph(
            adjacency_list=request.graph,
            method=request.method,
            k=request.k,
            r=request.r
        )
        
        return {"coloring": color_assignment}
    except Exception as e:
        logger.error(f"Error in assign_colors: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/circulant/antiprism")
async def antiprism_assignment(request: AntiprismRequest) -> Dict[str, Dict[int, int]]:
    """
    Assign colors to an antiprism graph.
    
    Args:
        request: The antiprism coloring request
        
    Returns:
        Dictionary mapping vertices to their assigned colors
    """
    try:
        logger.info(f'Antiprism Request: {request}')
        
        adjacency_matrix = create_antiprism_adjacency_matrix(request.n)
        adjacency_list = adjacency_matrix_to_adjacency_list(adjacency_matrix)
        logger.info(f'Adjacency List: {adjacency_list}')

        color_assignment = ColoringService.color_graph(
            adjacency_list=adjacency_list,
            method=request.method,
            k=request.k,
            r=request.r
        )
        
        return {"coloring": color_assignment}
    except Exception as e:
        logger.error(f"Error in antiprism_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch/circulant/antiprism")
async def antiprism_batch_assignment(request: AntiprismBatchRequest) -> Dict[int, Dict[int, Dict[int, int]]]:
    """
    Process a batch of antiprism coloring requests.
    
    Args:
        request: The batch request containing parameters for multiple colorings
        
    Returns:
        Nested dictionary of color assignments: {r: {n: color_assignment}}
    """
    try:
        return ColoringService.process_antiprism_batch(request)
    except Exception as e:
        logger.error(f"Error in antiprism_batch_assignment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
