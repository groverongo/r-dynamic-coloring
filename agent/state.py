"""LangGraph state definition for the graph analysis agent."""

from typing import Annotated, Any, Dict, List, Literal, Optional
from typing_extensions import TypedDict
import operator
import networkx as nx


class GraphState(TypedDict):
    """State schema for the graph analysis agent.
    
    This state is maintained throughout the LangGraph workflow and contains
    all information about the current graph, user queries, and analysis results.
    """
    
    # Graph Representation
    # Graph Representation
    graph_data: Optional[Dict[str, Any]]
    """The dictionary representation of the graph (node-link data) for serialization."""
    
    input_format: Optional[Literal["adjacency_list", "adjacency_matrix", "image"]]
    """The format used to input the graph."""
    
    raw_input: Optional[Any]
    """The original raw input (dict, list, or image path) for reference."""
    
    # Coloring Information
    coloring: Optional[Dict[str, str]]
    """Node coloring assignment: {node_id: color}."""
    
    edge_coloring: Optional[Dict[tuple[str, str], str]]
    """Edge coloring assignment: {(node1, node2): color}."""
    
    # Conversation & Query Tracking
    messages: Annotated[List[Dict[str, Any]], operator.add]
    """Conversation history with the agent."""
    
    current_query: Optional[str]
    """The current user query being processed."""
    
    query_type: Optional[Literal["question", "visualization", "analysis", "coloring"]]
    """Type of the current query."""
    
    # Analysis Results
    analysis_results: Optional[Dict[str, Any]]
    """Results from graph theory analysis computations."""
    
    # Visualization
    last_visualization_path: Optional[str]
    """Path to the most recently generated visualization."""
    
    visualization_params: Optional[Dict[str, Any]]
    """Parameters used for the last visualization."""
    
    # Knowledge & Context
    custom_sources: Annotated[List[str], operator.add]
    """Custom learning sources provided by the user (file paths or content)."""
    
    state_specific_context: Optional[str]
    """Temporary context for the current request only."""
    
    # Metadata
    session_id: Optional[str]
    """Unique identifier for the current session."""
    
    error: Optional[str]
    """Error message if something went wrong."""
    
    next_action: Optional[str]
    """Suggested next action for routing."""


def create_initial_state(session_id: Optional[str] = None) -> GraphState:
    """Create an initial empty state for the agent.
    
    Args:
        session_id: Optional session identifier
        
    Returns:
        Initial GraphState with default values
    """
    return GraphState(
        graph_data=None,
        input_format=None,
        raw_input=None,
        coloring=None,
        edge_coloring=None,
        messages=[],
        current_query=None,
        query_type=None,
        analysis_results=None,
        last_visualization_path=None,
        visualization_params=None,
        custom_sources=[],
        state_specific_context=None,
        session_id=session_id,
        error=None,
        next_action=None,
    )
