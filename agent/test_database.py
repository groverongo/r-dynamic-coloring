"""Test SQLite session database functionality."""

import sys
import networkx as nx

from database import db
from graph_parsers import parse_adjacency_list

def test_save_and_load_session():
    """Test saving and loading a session."""
    print("Testing save and load...")
    
    # Create a test graph
    adj_list = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
    graph = parse_adjacency_list(adj_list)
    
    # Create session state
    state = {
        "graph": graph,
        "input_format": "adjacency_list",
        "raw_input": adj_list,
        "coloring": {"A": "red", "B": "blue", "C": "green"},
        "messages": [
            {"role": "user", "content": "Load graph"},
            {"role": "assistant", "content": "Graph loaded!"}
        ],
        "analysis_results": {"num_nodes": 3},
        "session_id": "test-session-1",
    }
    
    # Save session
    success = db.save_session("test-session-1", state)
    assert success, "Failed to save session"
    print("  ✓ Session saved")
    
    # Load session
    loaded_state = db.load_session("test-session-1")
    assert loaded_state is not None, "Failed to load session"
    print("  ✓ Session loaded")
    
    # Verify data
    assert loaded_state["input_format"] == "adjacency_list"
    assert loaded_state["coloring"]["A"] == "red"
    assert len(loaded_state["messages"]) == 2
    assert loaded_state["graph"].number_of_nodes() == 3
    print("  ✓ Data verified")
    
    print("✅ Save and load test passed!\n")


def test_update_session():
    """Test updating an existing session."""
    print("Testing session update...")
    
    # Load existing session
    state = db.load_session("test-session-1")
    assert state is not None
    
    # Update it
    state["messages"].append({"role": "user", "content": "Analyze graph"})
    state["analysis_results"] = {"chromatic_number": 3}
    
    success = db.save_session("test-session-1", state)
    assert success, "Failed to update session"
    print("  ✓ Session updated")
    
    # Reload and verify
    reloaded = db.load_session("test-session-1")
    assert len(reloaded["messages"]) == 3
    assert reloaded["analysis_results"]["chromatic_number"] == 3
    print("  ✓ Update verified")
    
    print("✅ Update test passed!\n")


def test_list_sessions():
    """Test listing sessions."""
    print("Testing list sessions...")
    
    # Create another session
    state2 = {
        "graph": None,
        "messages": [],
        "session_id": "test-session-2",
    }
    db.save_session("test-session-2", state2)
    
    # List sessions
    sessions = db.list_sessions()
    assert len(sessions) >= 2, "Should have at least 2 sessions"
    print(f"  ✓ Found {len(sessions)} sessions")
    
    for session in sessions[:5]:
        print(f"     - {session['session_id']}: Updated {session['updated_at']}")
    
    print("✅ List test passed!\n")


def test_delete_session():
    """Test deleting a session."""
    print("Testing session deletion...")
    
    # Delete test session 2
    success = db.delete_session("test-session-2")
    assert success, "Failed to delete session"
    print("  ✓ Session deleted")
    
    # Verify it's gone
    loaded = db.load_session("test-session-2")
    assert loaded is None, "Session should be deleted"
    print("  ✓ Deletion verified")
    
    print("✅ Delete test passed!\n")


def test_persistence():
    """Test that sessions persist across database instances."""
    print("Testing persistence...")
    
    # Load session from original database instance
    state1 = db.load_session("test-session-1")
    assert state1 is not None
    
    # Create a new database instance
    from database import SessionDatabase
    db2 = SessionDatabase()
    
    # Load same session
    state2 = db2.load_session("test-session-1")
    assert state2 is not None, "Session should persist"
    assert state2["input_format"] == state1["input_format"]
    print("  ✓ Session persists across instances")
    
    print("✅ Persistence test passed!\n")


def cleanup():
    """Cleanup test sessions."""
    print("Cleaning up test sessions...")
    db.delete_session("test-session-1")
    db.delete_session("test-session-2")
    print("  ✓ Cleanup complete\n")


if __name__ == "__main__":
    print("=" * 70)
    print("SQLite Session Database Tests")
    print("=" * 70 + "\n")
    
    try:
        test_save_and_load_session()
        test_update_session()
        test_list_sessions()
        test_delete_session()
        test_persistence()
        
        print("=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        print("\nDatabase location:", db.db_path)
        print("Total sessions:", len(db.list_sessions()))
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        cleanup()
