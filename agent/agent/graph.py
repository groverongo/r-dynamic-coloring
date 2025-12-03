"""LangGraph workflow definition for the graph analysis agent."""

from typing import Dict, Any, Optional, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from pathlib import Path

from state import GraphState, create_initial_state
from agent.nodes import (
    process_input_node,
    process_coloring_node,
    generate_visualization_node,
    answer_question_node,
    analyze_graph_node,
    route_request_node,
)
from config import config


# Initialize checkpoint saver
checkpoint_db_path = config.VISUALIZATION_DIR.parent / "checkpoints.db"
checkpointer = SqliteSaver.from_conn_string(str(checkpoint_db_path))


def should_process_input(state: GraphState) -> Literal["process_input", "route"]:
    """Decide if we need to process input or route the request."""
    if state.get("raw_input") and not state.get("graph_data"):
        return "process_input"
    return "route"


def route_after_routing(state: GraphState) -> Literal["visualize", "analyze", "answer", "end"]:
    """Route to the appropriate node based on next_action."""
    next_action = state.get("next_action", "answer")
    
    if next_action == "visualize":
        return "visualize"
    elif next_action == "analyze":
        return "analyze"
    elif next_action == "answer":
        return "answer"
    else:
        return "end"


def create_graph() -> StateGraph:
    """Create the LangGraph workflow.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("process_input", process_input_node)
    workflow.add_node("process_coloring", process_coloring_node)
    workflow.add_node("route", route_request_node)
    workflow.add_node("visualize", generate_visualization_node)
    workflow.add_node("analyze", analyze_graph_node)
    workflow.add_node("answer", answer_question_node)
    
    # Define the flow
    # Start with input processing check
    workflow.set_conditional_entry_point(
        should_process_input,
        {
            "process_input": "process_input",
            "route": "route",
        }
    )
    
    # After input processing, check for coloring
    workflow.add_conditional_edges(
        "process_input",
        lambda state: "process_coloring" if state.get("coloring") or state.get("edge_coloring") else "route",
        {
            "process_coloring": "process_coloring",
            "route": "route",
        }
    )
    
    # After coloring, go to routing
    workflow.add_edge("process_coloring", "route")
    
    # Route to appropriate action
    workflow.add_conditional_edges(
        "route",
        route_after_routing,
        {
            "visualize": "visualize",
            "analyze": "analyze",
            "answer": "answer",
            "end": END,
        }
    )
    
    # All action nodes end the workflow
    workflow.add_edge("visualize", END)
    workflow.add_edge("analyze", END)
    workflow.add_edge("answer", END)
    
    # Compile with checkpointer for state persistence
    return workflow.compile(checkpointer=checkpointer)


# Create the compiled graph
graph = create_graph()


def run_agent(
    user_input: str = None,
    graph_input: dict = None,
    input_format: str = None,
    coloring: dict = None,
    session_id: str = "default",
    state_specific_context: str = None,
) -> GraphState:
    """Run the agent with given inputs.
    
    Args:
        user_input: User's question or request
        graph_input: Graph data (adjacency list/matrix/image)
        input_format: Format of graph input ("adjacency_list", "adjacency_matrix", "image")
        coloring: Optional node coloring
        session_id: Session identifier for state persistence
        state_specific_context: Additional context for this request
        
    Returns:
        Final state after processing
    """
    # Create inputs
    inputs = {}
    
    # Always set session_id
    inputs["session_id"] = session_id
    
    # Populate inputs
    if user_input:
        inputs["current_query"] = user_input
        # Initialize messages if this is the first run, or append if it's a list
        # But since we are passing inputs to invoke, we should pass the new message
        # LangGraph will handle the reducer for messages
        inputs["messages"] = [{
            "role": "user",
            "content": user_input,
        }]
    
    if graph_input:
        inputs["raw_input"] = graph_input
        inputs["input_format"] = input_format
    
    if coloring:
        inputs["coloring"] = coloring
    
    if state_specific_context:
        inputs["state_specific_context"] = state_specific_context
    
    # Run the graph
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke(inputs, config)
    
    return result
