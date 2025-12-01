"""Pydantic schemas for API requests and responses."""

from typing import Dict, List, Optional, Literal, Union, Any
from pydantic import BaseModel, Field


# Input Schemas

class AdjacencyListInput(BaseModel):
    """Schema for adjacency list graph input."""
    adjacency_list: Dict[str, List[str]] = Field(
        ...,
        description="Graph as adjacency list: {node_id: [neighbor_ids]}",
        examples=[{"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}]
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier for maintaining state"
    )


class AdjacencyMatrixInput(BaseModel):
    """Schema for adjacency matrix graph input."""
    adjacency_matrix: List[List[Union[int, str]]] = Field(
        ...,
        description="Graph as adjacency matrix",
        examples=[[[0, 1, 1], [1, 0, 1], [1, 1, 0]]]
    )
    node_labels: Optional[List[str]] = Field(
        default=None,
        description="Optional node labels. If not provided, uses indices."
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier for maintaining state"
    )


class GraphImageInput(BaseModel):
    """Schema for image-based graph input."""
    image_path: Optional[str] = Field(
        default=None,
        description="Path to saved image file"
    )
    image_url: Optional[str] = Field(
        default=None,
        description="URL to image"
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier for maintaining state"
    )


class ColoringInput(BaseModel):
    """Schema for coloring assignment."""
    coloring: Dict[str, str] = Field(
        ...,
        description="Node coloring: {node_id: color}",
        examples=[{"A": "red", "B": "blue", "C": "red"}]
    )
    edge_coloring: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional edge coloring: {'node1-node2': color}"
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier"
    )


# Query Schemas

class QueryRequest(BaseModel):
    """Schema for user queries."""
    query: str = Field(
        ...,
        description="User's question or request",
        examples=["What is the chromatic number of this graph?"]
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier"
    )
    state_specific_context: Optional[str] = Field(
        default=None,
        description="Additional context for this query only"
    )


class VisualizationRequest(BaseModel):
    """Schema for visualization requests."""
    layout: Optional[Literal["spring", "circular", "kamada_kawai", "planar", "shell", "spectral"]] = Field(
        default="spring",
        description="Layout algorithm to use"
    )
    title: Optional[str] = Field(
        default=None,
        description="Title for the visualization"
    )
    highlight_nodes: Optional[List[str]] = Field(
        default=None,
        description="List of nodes to highlight"
    )
    highlight_edges: Optional[List[List[str]]] = Field(
        default=None,
        description="List of edges to highlight as [node1, node2] pairs"
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier"
    )


class AnalysisRequest(BaseModel):
    """Schema for analysis requests."""
    analysis_type: Optional[Literal["comprehensive", "basic", "centrality", "chromatic", "connectivity"]] = Field(
        default="comprehensive",
        description="Type of analysis to perform"
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Session identifier"
    )


# Response Schemas

class GraphResponse(BaseModel):
    """Response after graph input."""
    success: bool
    message: str
    num_nodes: Optional[int] = None
    num_edges: Optional[int] = None
    session_id: str
    error: Optional[str] = None


class QueryResponse(BaseModel):
    """Response to user queries."""
    success: bool
    answer: Optional[str] = None
    session_id: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    error: Optional[str] = None


class VisualizationResponse(BaseModel):
    """Response with visualization."""
    success: bool
    visualization_path: Optional[str] = None
    message: str
    session_id: str
    error: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response with analysis results."""
    success: bool
    analysis_results: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    session_id: str
    error: Optional[str] = None


class SourceUploadResponse(BaseModel):
    """Response after source upload."""
    success: bool
    message: str
    source_id: Optional[str] = None
    error: Optional[str] = None
