"""Session management using LangGraph checkpoints."""

from typing import Optional, Dict, Any, List
from langgraph.checkpoint.sqlite import SqliteSaver
from pathlib import Path

from config import config


# Use the same checkpoint database as the workflow
checkpoint_db_path = config.VISUALIZATION_DIR.parent / "checkpoints.db"
checkpointer = SqliteSaver.from_conn_string(str(checkpoint_db_path))


def list_sessions(limit: int = 100) -> List[Dict[str, Any]]:
    """List all checkpoint threads (sessions).
    
    Args:
        limit: Maximum number of sessions to return
        
    Returns:
        List of session metadata
    """
    # Note: LangGraph checkpoints are organized by thread_id
    # We can list checkpoints but the API is different from our custom implementation
    # For now, we'll return a placeholder
    # In practice, you'd query the checkpoint database directly
    return []


def get_session_state(session_id: str) -> Optional[Dict[str, Any]]:
    """Get the current state for a session.
    
    Args:
        session_id: The thread_id/session_id
        
    Returns:
        The latest checkpoint state or None
    """
    try:
        # Get the latest checkpoint for this thread
        config_dict = {"configurable": {"thread_id": session_id}}
        checkpoint = checkpointer.get(config_dict)
        
        if checkpoint:
            return checkpoint.get("channel_values", {})
        return None
    except Exception as e:
        print(f"Error getting session state: {e}")
        return None


def delete_session(session_id: str) -> bool:
    """Delete all checkpoints for a session.
    
    Args:
        session_id: The thread_id/session_id
        
    Returns:
        True if successful
    """
    # LangGraph checkpoint doesn't have a built-in delete
    # We'd need to directly manipulate the SQLite database
    # For now, this is a placeholder
    return False


def cleanup_old_sessions(days: int = 7) -> int:
    """Delete checkpoints older than specified days.
    
    Args:
        days: Number of days to keep
        
    Returns:
        Number of sessions deleted
    """
    # This would require direct SQLite access
    # Placeholder for now
    return 0
