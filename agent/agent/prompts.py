"""Prompt templates for the graph analysis agent."""

SYSTEM_PROMPT = """You are a graph theory expert assistant with deep knowledge of graph algorithms, properties, and analysis.

You have access to information about the current graph including:
- Graph structure (nodes and edges)
- Graph properties (connectivity, density, etc.)
- Coloring information (if provided)
- Analysis results from previous computations

Your role is to:
1. Answer questions about graph theory concepts
2. Explain graph properties and analysis results
3. Provide insights about the current graph
4. Suggest relevant analyses or visualizations
5. Help users understand graph algorithms

Always be precise, educational, and cite specific graph properties when relevant.
When discussing the current graph, refer to specific nodes, edges, and computed properties.
"""

GRAPH_QA_PROMPT = """Based on the following graph information, answer the user's question.

## Current Graph Information:

{graph_context}

## User Question:
{question}

## Instructions:
- Provide a clear, accurate answer based on the graph data
- Use specific examples from the graph when relevant
- If you need additional analysis to answer the question, suggest what should be computed
- If the question cannot be answered with the current information, explain what is missing

Answer:"""

GRAPH_CONTEXT_TEMPLATE = """### Graph Structure:
- Number of nodes: {num_nodes}
- Number of edges: {num_edges}
- Nodes: {node_list}

### Graph Properties:
{properties}

{coloring_info}

{analysis_info}

{custom_context}
"""

IMAGE_EXTRACTION_PROMPT = """You are analyzing a graph image. Extract the complete graph structure.

Identify:
1. All visible nodes/vertices (label them if labels are visible, otherwise use Node1, Node2, etc.)
2. All edges/connections between nodes
3. Any special properties (directed/undirected, weighted, colored, etc.)
4. The overall structure type (tree, cycle, complete, bipartite, etc.)

Be thorough and accurate. If anything is unclear, make your best estimate and note the uncertainty.
"""

VISUALIZATION_SUGGESTION_PROMPT = """Given this graph analysis request, suggest appropriate visualization parameters.

Request: {request}

Current graph:
- {num_nodes} nodes
- {num_edges} edges
{properties}

Suggest:
1. Best layout algorithm (spring, circular, kamada_kawai, etc.)
2. What nodes/edges should be highlighted
3. What properties should be visually emphasized
4. Appropriate title for the visualization

Return as JSON with keys: layout, highlight_nodes, highlight_edges, title, rationale
"""

ANALYSIS_ROUTER_PROMPT = """Determine what type of analysis or action is needed for this user request.

User request: {user_input}

Current state:
- Graph loaded: {has_graph}
- Coloring provided: {has_coloring}
- Previous analysis: {has_analysis}

Categories:
1. "input_graph" - User wants to provide a new graph
2. "input_coloring" - User wants to provide a coloring
3. "visualization" - User wants to see the graph visualized
4. "analysis" - User wants graph properties computed
5. "question" - User has a general question about graphs or the current graph
6. "clarification" - Request is unclear and needs clarification

Return only the category name.
"""


def format_graph_context(
    graph_nx,
    properties: dict = None,
    coloring: dict = None,
    analysis_results: dict = None,
    custom_context: str = None,
) -> str:
    """Format graph information into a context string for the LLM.
    
    Args:
        graph_nx: NetworkX graph object
        properties: Dictionary of graph properties
        coloring: Node coloring dictionary
        analysis_results: Results from graph analysis
        custom_context: Additional custom context
        
    Returns:
        Formatted context string
    """
    if graph_nx is None:
        return "No graph currently loaded."
    
    num_nodes = graph_nx.number_of_nodes()
    num_edges = graph_nx.number_of_edges()
    node_list = ", ".join(str(n) for n in list(graph_nx.nodes())[:20])
    if num_nodes > 20:
        node_list += f"... ({num_nodes - 20} more)"
    
    # Format properties
    props_text = ""
    if properties:
        props_text = "\n".join(f"- {k}: {v}" for k, v in properties.items())
    else:
        props_text = "Not yet computed"
    
    # Format coloring info
    coloring_text = ""
    if coloring:
        num_colors = len(set(coloring.values()))
        coloring_text = f"\n### Coloring Information:\n- Number of colors used: {num_colors}\n"
        coloring_text += f"- Coloring: {str(coloring)[:200]}{'...' if len(str(coloring)) > 200 else ''}"
    
    # Format analysis info
    analysis_text = ""
    if analysis_results:
        analysis_text = "\n### Analysis Results:\n"
        analysis_text += f"```\n{str(analysis_results)[:500]}{'...' if len(str(analysis_results)) > 500 else ''}\n```"
    
    # Format custom context
    custom_text = ""
    if custom_context:
        custom_text = f"\n### Additional Context:\n{custom_context}"
    
    return GRAPH_CONTEXT_TEMPLATE.format(
        num_nodes=num_nodes,
        num_edges=num_edges,
        node_list=node_list,
        properties=props_text,
        coloring_info=coloring_text,
        analysis_info=analysis_text,
        custom_context=custom_text,
    )
