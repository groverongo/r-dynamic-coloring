"""Query and analysis API endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import networkx as nx

from api.schemas import (
    QueryRequest,
    QueryResponse,
    VisualizationRequest,
    VisualizationResponse,
    AnalysisRequest,
    AnalysisResponse,
    ColoringInput,
    GraphResponse,
)
from agent.graph import run_agent
from api.routers.graph import router as graph_router
from checkpoint_manager import get_session_state
from tools.graph_analysis import compute_comprehensive_analysis, compute_basic_properties
from tools.graph_visualization import generate_graph_visualization
from config import config

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/coloring", response_model=GraphResponse)
async def set_coloring(data: ColoringInput):
    """Set node/edge coloring for the graph."""
    state = get_session_state(data.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    if not state.get("graph"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    # Run agent to update coloring (it will checkpoint automatically)
    result = run_agent(
        coloring=data.coloring,
        edge_coloring=data.edge_coloring,
        session_id=data.session_id,
    )
    
    num_colors = len(set(data.coloring.values()))
    
    return GraphResponse(
        success=True,
        message=f"Coloring applied with {num_colors} colors",
        session_id=data.session_id,
        num_nodes=result.get("graph").number_of_nodes() if result.get("graph") else 0,
        num_edges=result.get("graph").number_of_edges() if result.get("graph") else 0,
    )


@router.post("/ask", response_model=QueryResponse)
async def ask_question(data: QueryRequest):
    """Ask a question about the graph."""
    # LangGraph will load state automatically via checkpoint
    try:
        # Run agent with query (checkpoint handles state)
        result = run_agent(
            user_input=data.query,
            session_id=data.session_id,
            state_specific_context=data.state_specific_context,
        )
        
        # State is automatically saved to checkpoint
        
        # Get the response from messages
        messages = result.get("messages", [])
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        
        if assistant_messages:
            answer = assistant_messages[-1]["content"]
        else:
            answer = "I couldn't generate a response. Please try again."
        
        return QueryResponse(
            answer=answer,
            session_id=data.session_id,
            context_used=bool(result.get("graph")),
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visualize", response_model=VisualizationResponse)
async def visualize_graph(data: VisualizationRequest):
    """Generate a visualization of the graph."""
    state = get_session_state(data.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    if not state.get("graph"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    try:
        # Set visualization parameters
        viz_params = {
            "layout": data.layout,
            "title": data.title,
            "highlight_nodes": data.highlight_nodes,
        }
        
        # Convert edge list to tuples if provided
        if data.highlight_edges:
            viz_params["highlight_edges"] = [tuple(edge) for edge in data.highlight_edges]
        
        # Generate visualization
        viz_path = generate_graph_visualization(
            state["graph"],
            layout=data.layout,
            node_coloring=state.get("coloring"),
            edge_coloring=state.get("edge_coloring"),
            highlight_nodes=data.highlight_nodes,
            highlight_edges=viz_params.get("highlight_edges"),
            title=data.title,
        )
        
        # Update state via agent (to trigger checkpoint)
        run_agent(
            visualization_path=str(viz_path),
            session_id=data.session_id,
        )
        
        return VisualizationResponse(
            success=True,
            visualization_path=str(viz_path),
            session_id=data.session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualize/{session_id}")
async def get_visualization(session_id: str):
    """Retrieve the latest visualization for a session."""
    state = get_session_state(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    
    viz_path = state.get("last_visualization_path")
    
    if not viz_path or not Path(viz_path).exists():
        raise HTTPException(status_code=404, detail="No visualization found for this session")
    
    return FileResponse(viz_path, media_type="image/png")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_graph(data: AnalysisRequest):
    """Perform graph analysis."""
    state = get_session_state(data.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    if not state.get("graph"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    try:
        graph = state["graph"]
        
        if data.analysis_type == "comprehensive":
            analysis = compute_comprehensive_analysis(graph)
        elif data.analysis_type == "basic":
            analysis = {"basic": compute_basic_properties(graph)}
        else:
            # Can add more specific analysis types
            analysis = compute_comprehensive_analysis(graph)
        
        # Update state via agent to trigger checkpoint
        run_agent(
            analysis_results=analysis,
            session_id=data.session_id,
        )
        
        # Create summary
        if "basic_properties" in analysis:
            summary = f"Graph has {analysis['basic_properties']['num_nodes']} nodes and {analysis['basic_properties']['num_edges']} edges. "
            summary += f"Connected: {analysis['basic_properties']['is_connected']}. "
            if "chromatic_info" in analysis:
                summary += f"Estimated chromatic number: {analysis['chromatic_info']['estimated_chromatic_number']}."
        else:
            summary = "Analysis completed"
        
        return AnalysisResponse(
            success=True,
            analysis_results=analysis,
            summary=summary,
            session_id=data.session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
