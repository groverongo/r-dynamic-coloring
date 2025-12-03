"""Session management API endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from checkpoint_manager import get_session_state, list_sessions, cleanup_old_sessions

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionInfo(BaseModel):
    """Session information model."""
    session_id: str
    created_at: str = None
    updated_at: str = None
    input_format: str = None


class CleanupResponse(BaseModel):
    """Cleanup operation response."""
    deleted_count: int
    message: str


@router.get("/list", response_model=List[SessionInfo])
async def list_all_sessions(limit: int = 100):
    """List all sessions (limited functionality with LangGraph checkpoints)."""
    sessions_list = list_sessions(limit=limit)
    return [SessionInfo(**s) for s in sessions_list] if sessions_list else []


@router.delete("/cleanup")
async def cleanup_sessions(days: int = 7):
    """Delete sessions older than specified days."""
    deleted = cleanup_old_sessions(days=days)
    return CleanupResponse(
        deleted_count=deleted,
        message=f"Cleanup functionality requires direct SQLite access. Use SQL to clean checkpoints database."
    )


@router.get("/{session_id}")
async def get_session_details(session_id: str):
    """Get detailed information about a session."""
    state = get_session_state(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    
    graph = state.get("graph")
    
    return {
        "session_id": session_id,
        "has_graph": graph is not None,
        "num_nodes": graph.number_of_nodes() if graph else 0,
        "num_edges": graph.number_of_edges() if graph else 0,
        "input_format": state.get("input_format"),
        "has_coloring": bool(state.get("coloring")),
        "has_analysis": bool(state.get("analysis_results")),
        "num_messages": len(state.get("messages", [])),
        "last_visualization": state.get("last_visualization_path"),
    }
