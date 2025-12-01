"""API usage examples using requests library."""

import requests
import json


BASE_URL = "http://localhost:8000"


def example_api_adjacency_list():
    """Example: Load graph via API (adjacency list)."""
    print("=" * 60)
    print("API Example 1: Adjacency List")
    print("=" * 60)
    
    url = f"{BASE_URL}/graph/adjacency-list"
    data = {
        "adjacency_list": {
            "A": ["B", "C"],
            "B": ["A", "C"],
            "C": ["A", "B"]
        },
        "session_id": "api_session_1"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    print()


def example_api_coloring():
    """Example: Set coloring via API."""
    print("=" * 60)
    print("API Example 2: Set Coloring")
    print("=" * 60)
    
    url = f"{BASE_URL}/query/coloring"
    data = {
        "coloring": {
            "A": "red",
            "B": "blue",
            "C": "red"
        },
        "session_id": "api_session_1"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    print()


def example_api_question():
    """Example: Ask a question via API."""
    print("=" * 60)
    print("API Example 3: Ask Question")
    print("=" * 60)
    
    url = f"{BASE_URL}/query/ask"
    data = {
        "query": "What is the chromatic number of this graph?",
        "session_id": "api_session_1"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Question: {data['query']}")
    print(f"Answer: {result.get('answer', 'No answer')}")
    print()


def example_api_visualize():
    """Example: Generate and retrieve visualization."""
    print("=" * 60)
    print("API Example 4: Visualization")
    print("=" * 60)
    
    # Generate visualization
    url = f"{BASE_URL}/query/visualize"
    data = {
        "layout": "circular",
        "title": "Triangle Graph",
        "session_id": "api_session_1"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Generate Status: {response.status_code}")
    print(f"Visualization path: {result.get('visualization_path')}")
    
    # Retrieve visualization
    if result.get("success"):
        url = f"{BASE_URL}/query/visualize/api_session_1"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save the image
            with open("graph_visualization.png", "wb") as f:
                f.write(response.content)
            print("✓ Visualization saved to graph_visualization.png")
    print()


def example_api_analyze():
    """Example: Analyze graph via API."""
    print("=" * 60)
    print("API Example 5: Graph Analysis")
    print("=" * 60)
    
    url = f"{BASE_URL}/query/analyze"
    data = {
        "analysis_type": "comprehensive",
        "session_id": "api_session_1"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Summary: {result.get('summary')}")
    
    if result.get("analysis_results"):
        basic = result["analysis_results"].get("basic_properties", {})
        print(f"\nBasic Properties:")
        print(f"  - Nodes: {basic.get('num_nodes')}")
        print(f"  - Edges: {basic.get('num_edges')}")
        print(f"  - Connected: {basic.get('is_connected')}")
        print(f"  - Density: {basic.get('density')}")
    print()


def example_api_session_info():
    """Example: Get session information."""
    print("=" * 60)
    print("API Example 6: Session Info")
    print("=" * 60)
    
    url = f"{BASE_URL}/graph/info/api_session_1"
    response = requests.get(url)
    result = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    print()


def check_server():
    """Check if server is running."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Server is running")
            print(f"  Health check: {response.json()}\n")
            return True
        else:
            print("❌ Server returned unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it with:")
        print("   uv run uvicorn api.main:app --reload\n")
        return False


if __name__ == "__main__":
    print("\n🌟 Graph Analysis Agent - API Examples\n")
    
    if not check_server():
        exit(1)
    
    try:
        example_api_adjacency_list()
        example_api_coloring()
        example_api_question()
        example_api_visualize()
        example_api_analyze()
        example_api_session_info()
        
        print("=" * 60)
        print("✅ All API examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
