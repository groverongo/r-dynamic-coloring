"""Test the chat endpoint functionality."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routers.chat import extract_graph_from_message


def test_graph_extraction():
    """Test graph extraction from messages."""
    print("Testing graph extraction from messages...\n")
    
    # Test adjacency list
    msg1 = 'Here is my graph: {"A": ["B", "C"], "B": ["A"], "C": ["A"]}'
    result1 = extract_graph_from_message(msg1)
    print(f"Message: {msg1}")
    print(f"Extracted: {result1}")
    print(f"✓ Adjacency list detection: {'PASS' if result1 and result1['format'] == 'adjacency_list' else 'FAIL'}\n")
    
    # Test adjacency matrix
    msg2 = "Graph: [[0, 1, 1], [1, 0, 0], [1, 0, 0]]"
    result2 = extract_graph_from_message(msg2)
    print(f"Message: {msg2}")
    print(f"Extracted: {result2}")
    print(f"✓ Adjacency matrix detection: {'PASS' if result2 and result2['format'] == 'adjacency_matrix' else 'FAIL'}\n")
    
    # Test no graph
    msg3 = "What is a chromatic number?"
    result3 = extract_graph_from_message(msg3)
    print(f"Message: {msg3}")
    print(f"Extracted: {result3}")
    print(f"✓ No graph detection: {'PASS' if result3 is None else 'FAIL'}\n")


if __name__ == "__main__":
    print("=" * 70)
    print("Chat Endpoint Tests")
    print("=" * 70 + "\n")
    
    test_graph_extraction()
    
    print("=" * 70)
    print("✅ Tests complete!")
    print("=" * 70)
    print("\nTo test the full chat interface:")
    print("1. Start the server: uv run uvicorn api.main:app --reload")
    print("2. Run the CLI: uv run python chat_cli.py")
    print("3. Or open: chat_interface.html in your browser")
