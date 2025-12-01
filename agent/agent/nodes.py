"""LangGraph node implementations for the graph analysis agent."""

from typing import Any, Dict
import google.generativeai as genai
import networkx as nx

from state import GraphState
from config import config
from graph_parsers import parse_adjacency_list, parse_adjacency_matrix
from tools.graph_analysis import compute_comprehensive_analysis, compute_basic_properties
from tools.graph_visualization import generate_graph_visualization
from tools.image_parsing import parse_graph_from_image
from agent.prompts import (
    SYSTEM_PROMPT,
    GRAPH_QA_PROMPT,
    format_graph_context,
    ANALYSIS_ROUTER_PROMPT,
)


def setup_gemini():
    """Configure Gemini API."""
    genai.configure(api_key=config.GOOGLE_API_KEY)


def get_graph(state: GraphState) -> nx.Graph:
    """Helper to reconstruct graph from state."""
    if state.get("graph_data"):
        return nx.node_link_graph(state["graph_data"])
    return None


def set_graph(state: GraphState, graph: nx.Graph):
    """Helper to save graph to state."""
    state["graph_data"] = nx.node_link_data(graph)


def process_input_node(state: GraphState) -> GraphState:
    """Process graph input and update state.
    
    This node handles parsing of different graph input formats and
    updates the state with the NetworkX graph object.
    """
    print("→ Processing graph input...")
    
    try:
        if state.get("input_format") == "adjacency_list":
            graph = parse_adjacency_list(state["raw_input"])
            set_graph(state, graph)
            state["messages"].append({
                "role": "system",
                "content": f"Graph loaded from adjacency list: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges"
            })
            
        elif state.get("input_format") == "adjacency_matrix":
            node_labels = state.get("node_labels")
            graph = parse_adjacency_matrix(state["raw_input"], node_labels=node_labels)
            set_graph(state, graph)
            state["messages"].append({
                "role": "system",
                "content": f"Graph loaded from adjacency matrix: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges"
            })
            
        elif state.get("input_format") == "image":
            result = parse_graph_from_image(state["raw_input"])
            graph = parse_adjacency_list(result["adjacency_list"])
            set_graph(state, graph)
            state["messages"].append({
                "role": "system",
                "content": f"Graph extracted from image: {result['description']}"
            })
        
        # Compute basic properties after loading
        graph = get_graph(state)
        if graph:
            basic_props = compute_basic_properties(graph)
            if not state.get("analysis_results"):
                state["analysis_results"] = {}
            state["analysis_results"]["basic"] = basic_props
            
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Failed to process graph input: {str(e)}"
        state["messages"].append({
            "role": "system",
            "content": f"Error: {state['error']}"
        })
    
    return state


def process_coloring_node(state: GraphState) -> GraphState:
    """Process coloring assignment.
    
    Handles both node and edge colorings.
    """
    print("→ Processing coloring assignment...")
    
    if not state.get("graph_data"):
        state["error"] = "No graph loaded. Please load a graph first."
        return state
    
    # The coloring should already be in state["coloring"] or state["edge_coloring"]
    # This node just validates it
    
    if state.get("coloring"):
        state["messages"].append({
            "role": "system",
            "content": f"Node coloring applied with {len(set(state['coloring'].values()))} colors"
        })
    
    if state.get("edge_coloring"):
        state["messages"].append({
            "role": "system",
            "content": f"Edge coloring applied with {len(set(state['edge_coloring'].values()))} colors"
        })
    
    return state


def generate_visualization_node(state: GraphState) -> GraphState:
    """Generate graph visualization.
    
    Creates a visual representation of the graph using NetworkX and Matplotlib.
    """
    print("→ Generating visualization...")
    
    graph = get_graph(state)
    if not graph:
        state["error"] = "No graph to visualize. Please load a graph first."
        return state
    
    try:
        # Get visualization parameters from state or use defaults
        params = state.get("visualization_params", {})
        
        viz_path = generate_graph_visualization(
            graph,
            layout=params.get("layout", config.DEFAULT_GRAPH_LAYOUT),
            node_coloring=state.get("coloring"),
            edge_coloring=state.get("edge_coloring"),
            highlight_nodes=params.get("highlight_nodes"),
            highlight_edges=params.get("highlight_edges"),
            title=params.get("title"),
            figsize=params.get("figsize", config.DEFAULT_FIGURE_SIZE),
            node_size=params.get("node_size", config.DEFAULT_NODE_SIZE),
        )
        
        state["last_visualization_path"] = str(viz_path)
        state["messages"].append({
            "role": "system",
            "content": f"Visualization generated: {viz_path}"
        })
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Failed to generate visualization: {str(e)}"
        state["messages"].append({
            "role": "system",
            "content": f"Error: {state['error']}"
        })
    
    return state


def answer_question_node(state: GraphState) -> GraphState:
    """Answer user questions using Gemini.
    
    Uses the graph context and Gemini to provide informed answers about
    the graph and graph theory in general.
    """
    print("→ Answering question with Gemini...")
    
    setup_gemini()
    
    try:
        # Build context
        graph_context = format_graph_context(
            get_graph(state),
            properties=state.get("analysis_results", {}).get("basic"),
            coloring=state.get("coloring"),
            analysis_results=state.get("analysis_results"),
            custom_context=state.get("state_specific_context"),
        )
        
        # Format prompt
        prompt = GRAPH_QA_PROMPT.format(
            graph_context=graph_context,
            question=state["current_query"],
        )
        
        # Call Gemini
        model = genai.GenerativeModel(
            config.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        # Add to messages
        state["messages"].append({
            "role": "assistant",
            "content": answer,
        })
        state["error"] = None
        
    except Exception as e:
        error_msg = f"Failed to generate answer: {str(e)}"
        state["error"] = error_msg
        state["messages"].append({
            "role": "system",
            "content": f"Error: {error_msg}"
        })
    
    return state


def analyze_graph_node(state: GraphState) -> GraphState:
    """Perform comprehensive graph analysis.
    
    Runs various graph theory computations and stores results in state.
    """
    print("→ Analyzing graph properties...")
    
    graph = get_graph(state)
    if not graph:
        state["error"] = "No graph to analyze. Please load a graph first."
        return state
    
    try:
        analysis = compute_comprehensive_analysis(graph)
        state["analysis_results"] = analysis
        
        # Summarize key findings
        summary = f"Analysis complete:\n"
        summary += f"- {analysis['basic_properties']['num_nodes']} nodes, {analysis['basic_properties']['num_edges']} edges\n"
        summary += f"- Connected: {analysis['basic_properties']['is_connected']}\n"
        summary += f"- Estimated chromatic number: {analysis['chromatic_info']['estimated_chromatic_number']}\n"
        
        state["messages"].append({
            "role": "system",
            "content": summary
        })
        state["error"] = None
        
    except Exception as e:
        state["error"] = f"Analysis failed: {str(e)}"
        state["messages"].append({
            "role": "system",
            "content": f"Error: {state['error']}"
        })
    
    return state


def route_request_node(state: GraphState) -> GraphState:
    """Determine the next action based on user input.
    
    This node analyzes the user query and sets the next_action field
    to route to the appropriate node.
    """
    print("→ Routing request...")
    
    setup_gemini()
    
    try:
        prompt = ANALYSIS_ROUTER_PROMPT.format(
            user_input=state.get("current_query", ""),
            has_graph="yes" if state.get("graph_data") else "no",
            has_coloring="yes" if state.get("coloring") else "no",
            has_analysis="yes" if state.get("analysis_results") else "no",
        )
        
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        category = response.text.strip().lower()
        
        # Map category to next action
        if "visualization" in category:
            state["next_action"] = "visualize"
            state["query_type"] = "visualization"
        elif "analysis" in category:
            state["next_action"] = "analyze"
            state["query_type"] = "analysis"
        elif "question" in category:
            state["next_action"] = "answer"
            state["query_type"] = "question"
        elif "input_graph" in category:
            state["next_action"] = "input_graph"
        elif "input_coloring" in category:
            state["next_action"] = "input_coloring"
        else:
            # Default to question answering
            state["next_action"] = "answer"
            state["query_type"] = "question"
            
    except Exception as e:
        print(f"Routing error: {e}")
        # Default to answer on error
        state["next_action"] = "answer"
        state["query_type"] = "question"
    
    return state
