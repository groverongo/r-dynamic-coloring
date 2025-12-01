"""Basic usage examples for the graph analysis agent."""

from agent.graph import run_agent
import json


def example_1_adjacency_list():
    """Example 1: Load a graph from adjacency list and ask questions."""
    print("=" * 60)
    print("Example 1: Adjacency List + Questions")
    print("=" * 60)
    
    # Create a simple triangle graph
    adjacency_list = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B"]
    }
    
    # Load the graph
    result = run_agent(
        graph_input=adjacency_list,
        input_format="adjacency_list",
        session_id="example_1"
    )
    
    print(f"✓ Graph loaded: {result['graph'].number_of_nodes()} nodes, {result['graph'].number_of_edges()} edges")
    
    # Ask a question
    result = run_agent(
        user_input="Is this graph complete? What is its chromatic number?",
        session_id="example_1"
    )
    
    answer = result["messages"][-1]["content"]
    print(f"\nQ: Is this graph complete? What is its chromatic number?")
    print(f"A: {answer}\n")


def example_2_adjacency_matrix():
    """Example 2: Load a graph from adjacency matrix."""
    print("=" * 60)
    print("Example 2: Adjacency Matrix")
    print("=" * 60)
    
    # Create a path graph: 0-1-2-3
    adjacency_matrix = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    
    result = run_agent(
        graph_input=adjacency_matrix,
        input_format="adjacency_matrix",
        session_id="example_2"
    )
    
    print(f"✓ Graph loaded: {result['graph'].number_of_nodes()} nodes, {result['graph'].number_of_edges()} edges")
    
    # Analyze the graph
    result = run_agent(
        user_input="What type of graph is this? Describe its properties.",
        session_id="example_2"
    )
    
    answer = result["messages"][-1]["content"]
    print(f"\nQ: What type of graph is this?")
    print(f"A: {answer}\n")


def example_3_coloring():
    """Example 3: Apply a coloring and validate it."""
    print("=" * 60)
    print("Example 3: Graph Coloring")
    print("=" * 60)
    
    # Create a cycle graph C5
    adjacency_list = {
        "1": ["2", "5"],
        "2": ["1", "3"],
        "3": ["2", "4"],
        "4": ["3", "5"],
        "5": ["4", "1"]
    }
    
    result = run_agent(
        graph_input=adjacency_list,
        input_format="adjacency_list",
        session_id="example_3"
    )
    
    print(f"✓ Graph loaded: C5 (cycle of length 5)")
    
    # Apply a 3-coloring
    coloring = {
        "1": "red",
        "2": "blue",
        "3": "red",
        "4": "blue",
        "5": "green"
    }
    
    result = run_agent(
        graph_input=adjacency_list,
        input_format="adjacency_list",
        coloring=coloring,
        session_id="example_3"
    )
    
    print(f"✓ Coloring applied: {coloring}")
    
    # Ask about the coloring
    result = run_agent(
        user_input="Is this a valid 3-coloring? Can we color this graph with fewer colors?",
        session_id="example_3"
    )
    
    answer = result["messages"][-1]["content"]
    print(f"\nQ: Is this a valid 3-coloring? Can we use fewer colors?")
    print(f"A: {answer}\n")


def example_4_analysis():
    """Example 4: Comprehensive graph analysis."""
    print("=" * 60)
    print("Example 4: Graph Analysis")
    print("=" * 60)
    
    # Create a more complex graph
    adjacency_list = {
        "A": ["B", "C", "D"],
        "B": ["A", "C"],
        "C": ["A", "B", "D", "E"],
        "D": ["A", "C", "E"],
        "E": ["C", "D", "F"],
        "F": ["E"]
    }
    
    result = run_agent(
        graph_input=adjacency_list,
        input_format="adjacency_list",
        session_id="example_4"
    )
    
    print(f"✓ Graph loaded: {result['graph'].number_of_nodes()} nodes, {result['graph'].number_of_edges()} edges")
    
    # Get analysis
    from tools.graph_analysis import compute_comprehensive_analysis
    
    analysis = compute_comprehensive_analysis(result["graph"])
    
    print("\n📊 Basic Properties:")
    for key, value in analysis["basic_properties"].items():
        print(f"  - {key}: {value}")
    
    print("\n📈 Degree Information:")
    print(f"  - Min degree: {analysis['degree_info']['min_degree']}")
    print(f"  - Max degree: {analysis['degree_info']['max_degree']}")
    print(f"  - Avg degree: {analysis['degree_info']['avg_degree']:.2f}")
    print(f"  - Is regular: {analysis['degree_info']['is_regular']}")
    
    print("\n🎨 Chromatic Information:")
    print(f"  - Estimated chromatic number: {analysis['chromatic_info']['estimated_chromatic_number']}")
    print(f"  - Upper bound (Brooks): {analysis['chromatic_info']['upper_bound_brooks']}")
    
    print()


def example_5_visualization():
    """Example 5: Generate visualization."""
    print("=" * 60)
    print("Example 5: Visualization")
    print("=" * 60)
    
    # Create a star graph
    adjacency_list = {
        "center": ["1", "2", "3", "4", "5"],
        "1": ["center"],
        "2": ["center"],
        "3": ["center"],
        "4": ["center"],
        "5": ["center"]
    }
    
    result = run_agent(
        graph_input=adjacency_list,
        input_format="adjacency_list",
        session_id="example_5"
    )
    
    print(f"✓ Graph loaded: Star graph with 6 nodes")
    
    # Generate visualization
    from tools.graph_visualization import generate_graph_visualization
    
    viz_path = generate_graph_visualization(
        result["graph"],
        layout="spring",
        title="Star Graph",
        highlight_nodes=["center"]
    )
    
    print(f"✓ Visualization saved to: {viz_path}")
    print()


if __name__ == "__main__":
    print("\n🌟 Graph Analysis Agent - Usage Examples\n")
    
    try:
        example_1_adjacency_list()
        example_2_adjacency_matrix()
        example_3_coloring()
        example_4_analysis()
        example_5_visualization()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
