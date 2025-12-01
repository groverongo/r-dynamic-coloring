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
from api.routers.graph import sessions
from tools.graph_analysis import compute_comprehensive_analysis, compute_basic_properties
from tools.graph_visualization import generate_graph_visualization
from config import config

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/coloring", response_model=GraphResponse)
async def set_coloring(data: ColoringInput):
    """Set node/edge coloring for the graph."""
    if data.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    print(f"DEBUG: sessions keys: {list(sessions.keys())}")
    state = sessions[data.session_id]
    print(f"DEBUG: state keys: {list(state.keys())}")
    
    if not state.get("graph_data"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    # Update state with coloring
    state["coloring"] = data.coloring
    if data.edge_coloring:
        state["edge_coloring"] = data.edge_coloring
    
    sessions[data.session_id] = state
    
    num_colors = len(set(data.coloring.values()))
    
    return GraphResponse(
        success=True,
        message=f"Coloring applied with {num_colors} colors",
        session_id=data.session_id,
    )


@router.post("/ask", response_model=QueryResponse)
async def ask_question(data: QueryRequest):
    """Ask a question about the graph."""
    if data.session_id not in sessions:
        # Create new session if it doesn't exist
        sessions[data.session_id] = {}
    
    try:
        # Get current state
        current_state = sessions[data.session_id]
        
        # Run agent with query
        result = run_agent(
            user_input=data.query,
            session_id=data.session_id,
            state_specific_context=data.state_specific_context,
        )
        
        print(f"DEBUG: run_agent result keys: {list(result.keys())}")
        if "graph_data" in result:
            print(f"DEBUG: run_agent result has graph_data")
        else:
            print(f"DEBUG: run_agent result MISSING graph_data")
        
        # Update session
        sessions[data.session_id] = result
        
        if result.get("error"):
            return QueryResponse(
                success=False,
                session_id=data.session_id,
                error=result["error"],
            )
        
        # Get the last assistant message
        messages = result.get("messages", [])
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        
        answer = assistant_messages[-1]["content"] if assistant_messages else "No response generated"
        
        return QueryResponse(
            success=True,
            answer=answer,
            session_id=data.session_id,
            conversation_history=messages,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visualize", response_model=VisualizationResponse)
async def visualize_graph(data: VisualizationRequest):
    """Generate a visualization of the graph."""
    if data.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    state = sessions[data.session_id]
    
    if not state.get("graph_data"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    try:
        # Set visualization parameters in state
        viz_params = {
            "layout": data.layout,
            "title": data.title,
            "highlight_nodes": data.highlight_nodes,
        }
        
        # Convert edge list to tuples if provided
        if data.highlight_edges:
            viz_params["highlight_edges"] = [tuple(edge) for edge in data.highlight_edges]
        
        # Generate visualization
        graph = nx.node_link_graph(state["graph_data"])
        viz_path = generate_graph_visualization(
            graph,
            layout=data.layout,
            node_coloring=state.get("coloring"),
            edge_coloring=state.get("edge_coloring"),
            highlight_nodes=data.highlight_nodes,
            highlight_edges=viz_params.get("highlight_edges"),
            title=data.title,
        )
        
        # Update state
        state["last_visualization_path"] = str(viz_path)
        state["visualization_params"] = viz_params
        sessions[data.session_id] = state
        
        return VisualizationResponse(
            success=True,
            visualization_path=str(viz_path),
            message="Visualization generated successfully",
            session_id=data.session_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualize/{session_id}")
async def get_visualization(session_id: str):
    """Retrieve the latest visualization for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    viz_path = state.get("last_visualization_path")
    
    if not viz_path or not Path(viz_path).exists():
        raise HTTPException(status_code=404, detail="No visualization found for this session")
    
    return FileResponse(viz_path, media_type="image/png")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_graph(data: AnalysisRequest):
    """Perform graph analysis."""
    if data.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please load a graph first.")
    
    state = sessions[data.session_id]
    
    if not state.get("graph_data"):
        raise HTTPException(status_code=400, detail="No graph loaded in this session")
    
    try:
        graph = nx.node_link_graph(state["graph_data"])
        
        if data.analysis_type == "comprehensive":
            analysis = compute_comprehensive_analysis(graph)
        elif data.analysis_type == "basic":
            analysis = {"basic": compute_basic_properties(graph)}
        else:
            # Can add more specific analysis types
            analysis = compute_comprehensive_analysis(graph)
        
        # Update state
        state["analysis_results"] = analysis
        sessions[data.session_id] = state
        
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
