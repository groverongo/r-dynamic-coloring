"""Conversational chat API endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from agent.graph import run_agent
from api.routers.graph import sessions
from graph_parsers import parse_adjacency_list, parse_adjacency_matrix
from tools.graph_visualization import generate_graph_visualization
from tools.graph_analysis import compute_comprehensive_analysis

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Schema for chat messages."""
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(default="default", description="Session identifier")


class ChatResponse(BaseModel):
    """Schema for chat responses."""
    response: str = Field(..., description="Agent's response")
    session_id: str
    actions_taken: Optional[List[str]] = Field(default=None, description="Actions performed")
    visualization_path: Optional[str] = None
    analysis_results: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, str]]] = None


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(data: ChatMessage):
    """Send a message to the agent via chat interface.
    
    This endpoint processes natural language messages and automatically:
    - Detects graph input in various formats
    - Answers questions about graphs
    - Generates visualizations when requested
    - Performs analysis when needed
    """
    try:
        # Get or create session
        if data.session_id not in sessions:
            sessions[data.session_id] = {
                "graph": None,
                "messages": [],
                "coloring": None,
                "analysis_results": None,
            }
        
        current_state = sessions[data.session_id]
        actions_taken = []
        
        # Check if message contains graph data
        graph_input = extract_graph_from_message(data.message)
        
        if graph_input:
            # User is providing a graph
            result = run_agent(
                graph_input=graph_input["data"],
                input_format=graph_input["format"],
                session_id=data.session_id,
            )
            sessions[data.session_id] = result
            
            graph = result.get("graph")
            if graph:
                actions_taken.append(f"Loaded graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
                response = f"I've loaded your graph! It has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges. What would you like to know about it?"
            else:
                response = "I had trouble parsing the graph. Could you provide it in a different format?"
        
        elif "visualiz" in data.message.lower() or "show" in data.message.lower() or "draw" in data.message.lower():
            # User wants a visualization
            if not current_state.get("graph"):
                response = "I don't have a graph loaded yet. Please provide a graph first using an adjacency list or matrix."
            else:
                viz_path = generate_graph_visualization(
                    current_state["graph"],
                    title="Graph Visualization",
                    node_coloring=current_state.get("coloring"),
                )
                current_state["last_visualization_path"] = str(viz_path)
                sessions[data.session_id] = current_state
                actions_taken.append("Generated visualization")
                response = f"I've created a visualization of your graph! You can access it at: {viz_path}"
        
        elif "analyz" in data.message.lower() or "properties" in data.message.lower() or "chromatic" in data.message.lower():
            # User wants analysis
            if not current_state.get("graph"):
                response = "I don't have a graph loaded yet. Please provide a graph first."
            else:
                analysis = compute_comprehensive_analysis(current_state["graph"])
                current_state["analysis_results"] = analysis
                sessions[data.session_id] = current_state
                actions_taken.append("Performed comprehensive analysis")
                
                basic = analysis["basic_properties"]
                chromatic = analysis["chromatic_info"]
                response = f"""I've analyzed your graph! Here are the key properties:

📊 **Basic Properties:**
- Nodes: {basic['num_nodes']}
- Edges: {basic['num_edges']}
- Connected: {basic['is_connected']}
- Density: {basic['density']:.3f}
- Is tree: {basic['is_tree']}
- Is bipartite: {basic['is_bipartite']}

🎨 **Chromatic Number:**
- Estimated: {chromatic['estimated_chromatic_number']}
- Upper bound: {chromatic['upper_bound_brooks']}

What else would you like to know?"""
        
        else:
            # General question or chat
            result = run_agent(
                user_input=data.message,
                session_id=data.session_id,
            )
            sessions[data.session_id] = result
            
            # Get the last assistant message
            messages = result.get("messages", [])
            assistant_messages = [m for m in messages if m.get("role") == "assistant"]
            
            if assistant_messages:
                response = assistant_messages[-1]["content"]
                actions_taken.append("Answered question using Gemini")
            else:
                response = "I'm here to help with graph analysis! You can provide a graph, ask questions, request visualizations, or get analysis."
        
        # Add to conversation history
        current_state["messages"].append({"role": "user", "content": data.message})
        current_state["messages"].append({"role": "assistant", "content": response})
        
        return ChatResponse(
            response=response,
            session_id=data.session_id,
            actions_taken=actions_taken if actions_taken else None,
            visualization_path=current_state.get("last_visualization_path"),
            analysis_results=current_state.get("analysis_results"),
            conversation_history=current_state["messages"][-10:],  # Last 10 messages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get conversation history for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "messages": sessions[session_id].get("messages", []),
        "has_graph": sessions[session_id].get("graph") is not None,
    }


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    raise HTTPException(status_code=404, detail="Session not found")


def extract_graph_from_message(message: str) -> Optional[Dict[str, Any]]:
    """Extract graph data from a message if present.
    
    Looks for JSON-like structures that represent adjacency lists or matrices.
    """
    import re
    import json
    
    # Try to find JSON in the message
    # Look for dictionary-like structures (adjacency list)
    dict_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(dict_pattern, message)
    
    for match in matches:
        try:
            # Try to parse as adjacency list
            data = json.loads(match.replace("'", '"'))
            if isinstance(data, dict):
                # Check if it looks like an adjacency list
                if all(isinstance(v, list) for v in data.values()):
                    return {"data": data, "format": "adjacency_list"}
        except:
            pass
    
    # Look for array-like structures (adjacency matrix)
    array_pattern = r'\[\[.*?\]\]'
    matches = re.findall(array_pattern, message)
    
    for match in matches:
        try:
            data = json.loads(match.replace("'", '"'))
            if isinstance(data, list) and all(isinstance(row, list) for row in data):
                return {"data": data, "format": "adjacency_matrix"}
        except:
            pass
    
    return None
