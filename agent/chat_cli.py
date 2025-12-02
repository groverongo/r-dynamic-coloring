"""Terminal-based chat interface for the Graph Analysis Agent."""

import requests
import sys
import uuid
from typing import Optional

API_URL = "http://localhost:8000"
SESSION_ID = f"cli-{uuid.uuid4().hex[:8]}"


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print("🔷  GRAPH ANALYSIS AGENT - Chat Interface")
    print("=" * 70)
    print(f"Session ID: {SESSION_ID}")
    print("\nI can help you with:")
    print("  • Analyze graphs (provide as adjacency list or matrix)")
    print("  • Answer questions about graph theory")
    print("  • Generate visualizations")
    print("  • Compute properties (chromatic number, centrality, etc.)")
    print("\nCommands:")
    print("  /help    - Show this help message")
    print("  /clear   - Clear session")
    print("  /history - Show conversation history")
    print("  /quit    - Exit the chat")
    print("=" * 70 + "\n")


def print_help():
    """Print help message."""
    print("\n📖 HELP")
    print("-" * 70)
    print("Example queries:")
    print("  • 'What is a chromatic number?'")
    print("  • '{\"A\": [\"B\", \"C\"], \"B\": [\"A\"], \"C\": [\"A\"]}'  (adjacency list)")
    print("  • '[[0, 1, 1], [1, 0, 0], [1, 0, 0]]'  (adjacency matrix)")
    print("  • 'Analyze the graph'")
    print("  • 'Show me a visualization'")
    print("  • 'Is this graph bipartite?'")
    print("-" * 70 + "\n")


def send_message(message: str) -> Optional[dict]:
    """Send a message to the chat API."""
    try:
        response = requests.post(
            f"{API_URL}/chat/message",
            json={
                "message": message,
                "session_id": SESSION_ID
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: Server returned status {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API server at {API_URL}")
        print("   Make sure the server is running:")
        print("   $ uv run uvicorn api.main:app --reload\n")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_history() -> Optional[dict]:
    """Get conversation history."""
    try:
        response = requests.get(f"{API_URL}/chat/history/{SESSION_ID}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def clear_session() -> bool:
    """Clear the current session."""
    try:
        response = requests.delete(f"{API_URL}/chat/session/{SESSION_ID}")
        return response.status_code == 200
    except:
        return False


def format_response(data: dict):
    """Format and print the agent's response."""
    print("\n🤖 Assistant:")
    print("-" * 70)
    print(data["response"])
    
    if data.get("actions_taken"):
        print("\n📋 Actions taken:")
        for action in data["actions_taken"]:
            print(f"   ✓ {action}")
    
    if data.get("visualization_path"):
        print(f"\n📊 Visualization: {data['visualization_path']}")
    
    print("-" * 70 + "\n")


def main():
    """Run the chat interface."""
    print_banner()
    
    # Check if server is running
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code != 200:
            print("⚠️  Warning: API server may not be running properly\n")
    except:
        print("⚠️  Warning: Cannot connect to API server")
        print(f"   Expected at: {API_URL}")
        print("   Start with: uv run uvicorn api.main:app --reload\n")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    print("Type your message (or /help for examples, /quit to exit):\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command == '/quit' or command == '/exit':
                    print("\n👋 Goodbye!\n")
                    break
                
                elif command == '/help':
                    print_help()
                    continue
                
                elif command == '/clear':
                    if clear_session():
                        print("✓ Session cleared\n")
                    else:
                        print("❌ Failed to clear session\n")
                    continue
                
                elif command == '/history':
                    history = get_history()
                    if history:
                        print("\n📜 Conversation History:")
                        print("-" * 70)
                        for msg in history.get("messages", []):
                            role = "You" if msg["role"] == "user" else "Assistant"
                            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                            print(f"{role}: {content}")
                        print("-" * 70 + "\n")
                    else:
                        print("❌ Could not retrieve history\n")
                    continue
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("   Use /help to see available commands\n")
                    continue
            
            # Send message to API
            result = send_message(user_input)
            
            if result:
                format_response(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except EOFError:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
