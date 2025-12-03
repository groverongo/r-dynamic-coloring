"""SQLite database manager for session persistence."""

import sqlite3
import json
import pickle
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import networkx as nx
from contextlib import contextmanager

from config import config


class SessionDatabase:
    """Manage session persistence with SQLite."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize the database.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            db_path = config.VISUALIZATION_DIR.parent / "sessions.db"
        
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    graph_blob BLOB,
                    input_format TEXT,
                    raw_input TEXT,
                    coloring TEXT,
                    edge_coloring TEXT,
                    messages TEXT,
                    analysis_results TEXT,
                    last_visualization_path TEXT,
                    visualization_params TEXT,
                    custom_sources TEXT,
                    state_specific_context TEXT
                )
            """)
            
            # Index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_updated 
                ON sessions(updated_at DESC)
            """)
    
    def _serialize_graph(self, graph: Optional[nx.Graph]) -> Optional[bytes]:
        """Serialize a NetworkX graph to bytes."""
        if graph is None:
            return None
        return pickle.dumps(graph)
    
    def _deserialize_graph(self, blob: Optional[bytes]) -> Optional[nx.Graph]:
        """Deserialize bytes to a NetworkX graph."""
        if blob is None:
            return None
        return pickle.loads(blob)
    
    def save_session(self, session_id: str, state: Dict[str, Any]) -> bool:
        """Save or update a session.
        
        Args:
            session_id: Unique session identifier
            state: Session state dictionary
            
        Returns:
            True if successful
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Serialize complex objects
                graph_blob = self._serialize_graph(state.get("graph"))
                messages_json = json.dumps(state.get("messages", []))
                coloring_json = json.dumps(state.get("coloring")) if state.get("coloring") else None
                edge_coloring_json = json.dumps(state.get("edge_coloring")) if state.get("edge_coloring") else None
                analysis_json = json.dumps(state.get("analysis_results")) if state.get("analysis_results") else None
                viz_params_json = json.dumps(state.get("visualization_params")) if state.get("visualization_params") else None
                custom_sources_json = json.dumps(state.get("custom_sources", []))
                raw_input_json = json.dumps(state.get("raw_input")) if state.get("raw_input") else None
                
                # Check if session exists
                cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
                exists = cursor.fetchone() is not None
                
                if exists:
                    # Update existing session
                    cursor.execute("""
                        UPDATE sessions SET
                            updated_at = CURRENT_TIMESTAMP,
                            graph_blob = ?,
                            input_format = ?,
                            raw_input = ?,
                            coloring = ?,
                            edge_coloring = ?,
                            messages = ?,
                            analysis_results = ?,
                            last_visualization_path = ?,
                            visualization_params = ?,
                            custom_sources = ?,
                            state_specific_context = ?
                        WHERE session_id = ?
                    """, (
                        graph_blob,
                        state.get("input_format"),
                        raw_input_json,
                        coloring_json,
                        edge_coloring_json,
                        messages_json,
                        analysis_json,
                        state.get("last_visualization_path"),
                        viz_params_json,
                        custom_sources_json,
                        state.get("state_specific_context"),
                        session_id
                    ))
                else:
                    # Insert new session
                    cursor.execute("""
                        INSERT INTO sessions (
                            session_id, graph_blob, input_format, raw_input,
                            coloring, edge_coloring, messages, analysis_results,
                            last_visualization_path, visualization_params,
                            custom_sources, state_specific_context
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        session_id,
                        graph_blob,
                        state.get("input_format"),
                        raw_input_json,
                        coloring_json,
                        edge_coloring_json,
                        messages_json,
                        analysis_json,
                        state.get("last_visualization_path"),
                        viz_params_json,
                        custom_sources_json,
                        state.get("state_specific_context")
                    ))
                
                return True
                
        except Exception as e:
            print(f"Error saving session {session_id}: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session by ID.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session state dictionary or None if not found
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                # Deserialize data
                state = {
                    "graph": self._deserialize_graph(row["graph_blob"]),
                    "input_format": row["input_format"],
                    "raw_input": json.loads(row["raw_input"]) if row["raw_input"] else None,
                    "coloring": json.loads(row["coloring"]) if row["coloring"] else None,
                    "edge_coloring": json.loads(row["edge_coloring"]) if row["edge_coloring"] else None,
                    "messages": json.loads(row["messages"]) if row["messages"] else [],
                    "analysis_results": json.loads(row["analysis_results"]) if row["analysis_results"] else None,
                    "last_visualization_path": row["last_visualization_path"],
                    "visualization_params": json.loads(row["visualization_params"]) if row["visualization_params"] else None,
                    "custom_sources": json.loads(row["custom_sources"]) if row["custom_sources"] else [],
                    "state_specific_context": row["state_specific_context"],
                    "session_id": session_id,
                }
                
                return state
                
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if successful
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting session {session_id}: {e}")
            return False
    
    def list_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session metadata
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, created_at, updated_at, input_format
                    FROM sessions
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (limit,))
                
                sessions = []
                for row in cursor.fetchall():
                    sessions.append({
                        "session_id": row["session_id"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                        "input_format": row["input_format"],
                    })
                
                return sessions
                
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []
    
    def cleanup_old_sessions(self, days: int = 7) -> int:
        """Delete sessions older than specified days.
        
        Args:
            days: Number of days to keep sessions
            
        Returns:
            Number of sessions deleted
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM sessions
                    WHERE updated_at < datetime('now', '-' || ? || ' days')
                """, (days,))
                return cursor.rowcount
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")
            return 0


# Global database instance
db = SessionDatabase()
