"""Quick verification script to test the agent setup."""

import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import networkx as nx
        print("  ✓ NetworkX")
    except ImportError as e:
        print(f"  ❌ NetworkX: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("  ✓ Google Generative AI")
    except ImportError as e:
        print(f"  ❌ Google Generative AI: {e}")
        return False
    
    try:
        from fastapi import FastAPI
        print("  ✓ FastAPI")
    except ImportError as e:
        print(f"  ❌ FastAPI: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph
        print("  ✓ LangGraph")
    except ImportError as e:
        print(f"  ❌ LangGraph: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("  ✓ Matplotlib")
    except ImportError as e:
        print(f"  ❌ Matplotlib: {e}")
        return False
    
    return True


def test_local_modules():
    """Test that local modules can be imported."""
    print("\nTesting local modules...")
    
    try:
        from config import config
        print("  ✓ config")
    except ImportError as e:
        print(f"  ❌ config: {e}")
        return False
    
    try:
        from state import GraphState, create_initial_state
        print("  ✓ state")
    except ImportError as e:
        print(f"  ❌ state: {e}")
        return False
    
    try:
        from graph_parsers import parse_adjacency_list, parse_adjacency_matrix
        print("  ✓ graph_parsers")
    except ImportError as e:
        print(f"  ❌ graph_parsers: {e}")
        return False
    
    try:
        from tools.graph_visualization import generate_graph_visualization
        print("  ✓ tools.graph_visualization")
    except ImportError as e:
        print(f"  ❌ tools.graph_visualization: {e}")
        return False
    
    try:
        from tools.graph_analysis import compute_basic_properties
        print("  ✓ tools.graph_analysis")
    except ImportError as e:
        print(f"  ❌ tools.graph_analysis: {e}")
        return False
    
    try:
        from agent.graph import run_agent
        print("  ✓ agent.graph")
    except ImportError as e:
        print(f"  ❌ agent.graph: {e}")
        return False
    
    try:
        from api.main import app
        print("  ✓ api.main")
    except ImportError as e:
        print(f"  ❌ api.main: {e}")
        return False
    
    return True


def test_configuration():
    """Test configuration."""
    print("\nTesting configuration...")
    
    try:
        from config import config
        
        if config.GOOGLE_API_KEY:
            print("  ✓ GOOGLE_API_KEY is set")
        else:
            print("  ⚠️  GOOGLE_API_KEY is not set (required for runtime)")
        
        print(f"  ✓ Gemini model: {config.GEMINI_MODEL}")
        print(f"  ✓ Visualization dir: {config.VISUALIZATION_DIR}")
        print(f"  ✓ Sources dir: {config.SOURCES_DIR}")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_basic_functionality():
    """Test basic graph operations."""
    print("\nTesting basic functionality...")
    
    try:
        from graph_parsers import parse_adjacency_list
        import networkx as nx
        
        # Create a simple graph
        adj_list = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
        graph = parse_adjacency_list(adj_list)
        
        assert graph.number_of_nodes() == 3, "Expected 3 nodes"
        assert graph.number_of_edges() == 2, "Expected 2 edges"
        
        print("  ✓ Graph parsing works")
        
        # Test analysis
        from tools.graph_analysis import compute_basic_properties
        props = compute_basic_properties(graph)
        
        assert props["num_nodes"] == 3
        assert props["num_edges"] == 2
        
        print("  ✓ Graph analysis works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Basic functionality error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Graph Analysis Agent - Verification")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Local Modules", test_local_modules()))
    results.append(("Configuration", test_configuration()))
    results.append(("Basic Functionality", test_basic_functionality()))
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("✅ All tests passed! The agent is ready to use.")
        print()
        print("To start the server:")
        print("  uv run uvicorn api.main:app --reload")
        print()
        print("To run examples:")
        print("  uv run python examples/basic_usage.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
