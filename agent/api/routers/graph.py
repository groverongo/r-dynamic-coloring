"""Graph input API endpoints."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
import shutil
import networkx as nx

from api.schemas import (
    AdjacencyListInput,
    AdjacencyMatrixInput,
    GraphImageInput,
    GraphResponse,
)
from agent.graph import run_agent
from config import config

router = APIRouter(prefix="/graph", tags=["graph"])

# In-memory session storage (replace with proper database in production)
sessions = {}


@router.post("/adjacency-list", response_model=GraphResponse)
async def input_adjacency_list(data: AdjacencyListInput):
    """Accept graph as adjacency list."""
    try:
        result = run_agent(
            graph_input=data.adjacency_list,
            input_format="adjacency_list",
            session_id=data.session_id,
        )
        
        # Store session
        sessions[data.session_id] = result
        
        if result.get("error"):
            return GraphResponse(
                success=False,
                message="Failed to process adjacency list",
                session_id=data.session_id,
                error=result["error"],
            )

        graph_data = result.get("graph_data")
        graph = nx.node_link_graph(graph_data) if graph_data else None
        return GraphResponse(
            success=True,
            message="Graph loaded successfully from adjacency list",
            num_nodes=graph.number_of_nodes() if graph else 0,
            num_edges=graph.number_of_edges() if graph else 0,
            session_id=data.session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adjacency-matrix", response_model=GraphResponse)
async def input_adjacency_matrix(data: AdjacencyMatrixInput):
    """Accept graph as adjacency matrix."""
    try:
        # Prepare state with node labels if provided
        initial_state = {
            "raw_input": data.adjacency_matrix,
            "input_format": "adjacency_matrix",
        }
        
        if data.node_labels:
            initial_state["node_labels"] = data.node_labels
        
        result = run_agent(
            graph_input=data.adjacency_matrix,
            input_format="adjacency_matrix",
            session_id=data.session_id,
        )
        
        sessions[data.session_id] = result
        
        if result.get("error"):
            return GraphResponse(
                success=False,
                message="Failed to process adjacency matrix",
                session_id=data.session_id,
                error=result["error"],
            )
        
        graph_data = result.get("graph_data")
        graph = nx.node_link_graph(graph_data) if graph_data else None
        return GraphResponse(
            success=True,
            message="Graph loaded successfully from adjacency matrix",
            num_nodes=graph.number_of_nodes() if graph else 0,
            num_edges=graph.number_of_edges() if graph else 0,
            session_id=data.session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image", response_model=GraphResponse)
async def input_graph_image(file: UploadFile = File(...), session_id: str = "default"):
    """Accept graph as an uploaded image."""
    try:
        # Save uploaded file
        upload_path = config.VISUALIZATION_DIR / f"upload_{session_id}_{file.filename}"
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process with agent
        result = run_agent(
            graph_input=str(upload_path),
            input_format="image",
            session_id=session_id,
        )
        
        sessions[session_id] = result
        
        if result.get("error"):
            return GraphResponse(
                success=False,
                message="Failed to extract graph from image",
                session_id=session_id,
                error=result["error"],
            )
        
        graph_data = result.get("graph_data")
        graph = nx.node_link_graph(graph_data) if graph_data else None
        return GraphResponse(
            success=True,
            message="Graph extracted successfully from image",
            num_nodes=graph.number_of_nodes() if graph else 0,
            num_edges=graph.number_of_edges() if graph else 0,
            session_id=session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/{session_id}")
async def get_graph_info(session_id: str):
    """Get information about the current graph in a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    graph_data = state.get("graph_data")
    graph = nx.node_link_graph(graph_data) if graph_data else None
    
    if not graph:
        return {"message": "No graph loaded in this session"}
    
    return {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "nodes": list(graph.nodes()),
        "input_format": state.get("input_format"),
        "has_coloring": bool(state.get("coloring")),
        "has_analysis": bool(state.get("analysis_results")),
    }
