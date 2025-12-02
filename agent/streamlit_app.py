"""Streamlit chat interface for the Graph Analysis Agent."""

import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Graph Analysis Agent",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        animation: slideIn 0.3s ease-out;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background: #f0f0f0;
        color: #333;
        margin-right: 20%;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """👋 Hello! I'm your Graph Analysis Agent. I can help you with:

• Analyze graphs (provide as adjacency list or matrix)
• Answer questions about graph theory
• Generate visualizations
• Compute properties (chromatic number, centrality, etc.)

Try asking me something or use the examples in the sidebar!"""
    }]

if "graph_loaded" not in st.session_state:
    st.session_state.graph_loaded = False

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "last_visualization" not in st.session_state:
    st.session_state.last_visualization = None


def check_api_health():
    """Check if the API server is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def send_message(message: str):
    """Send a message to the chat API."""
    try:
        response = requests.post(
            f"{API_URL}/chat/message",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Update session state
            if "graph" in message.lower() or "{" in message:
                st.session_state.graph_loaded = True
            
            if data.get("analysis_results"):
                st.session_state.last_analysis = data["analysis_results"]
            
            if data.get("visualization_path"):
                st.session_state.last_visualization = data["visualization_path"]
            
            return data
        else:
            return {"response": f"Error: Server returned status {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"response": f"⚠️ Cannot connect to API server at {API_URL}\n\nPlease start the server:\n```bash\nuv run uvicorn api.main:app --reload\n```"}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


def display_message(role: str, content: str):
    """Display a chat message."""
    css_class = "user-message" if role == "user" else "assistant-message"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{'You' if role == 'user' else '🤖 Agent'}:</strong><br/>
        {content.replace('\n', '<br/>')}
    </div>
    """, unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.title("🔷 Graph Analysis Agent")
    st.markdown("---")
    
    # Server status
    if check_api_health():
        st.success("✅ API Server Connected")
    else:
        st.error("❌ API Server Offline")
        st.info("Start with:\n```bash\nuv run uvicorn api.main:app --reload\n```")
    
    st.markdown("---")
    
    # Session info
    st.subheader("Session Info")
    st.text(f"ID: {st.session_state.session_id}")
    st.text(f"Messages: {len(st.session_state.messages)}")
    if st.session_state.graph_loaded:
        st.success("📊 Graph Loaded")
    
    st.markdown("---")
    
    # Example buttons
    st.subheader("📝 Quick Examples")
    
    if st.button("💡 What is a chromatic number?"):
        st.session_state.current_input = "What is a chromatic number?"
        st.rerun()
    
    if st.button("📈 Load sample graph"):
        st.session_state.current_input = '{"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}'
        st.rerun()
    
    if st.button("🔍 Analyze graph"):
        st.session_state.current_input = "Analyze the graph"
        st.rerun()
    
    if st.button("🎨 Show visualization"):
        st.session_state.current_input = "Show me a visualization"
        st.rerun()
    
    if st.button("❓ Is it bipartite?"):
        st.session_state.current_input = "Is this graph bipartite?"
        st.rerun()
    
    st.markdown("---")
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Conversation cleared! How can I help you?"
        }]
        st.session_state.graph_loaded = False
        st.session_state.last_analysis = None
        st.session_state.last_visualization = None
        st.rerun()
    
    st.markdown("---")
    
    # Info section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Graph Analysis Agent**
        
        Powered by:
        - LangGraph for workflow
        - Google Gemini AI
        - NetworkX for analysis
        - FastAPI backend
        
        **Capabilities:**
        - Natural language Q&A
        - Graph visualization
        - Chromatic number computation
        - Centrality analysis
        - And much more!
        """)

# Main chat area
st.title("💬 Graph Analysis Chat")

# Display chat history
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Show analysis if available
if st.session_state.last_analysis:
    with st.expander("📊 Latest Analysis Results", expanded=False):
        st.json(st.session_state.last_analysis)

# Show visualization if available
if st.session_state.last_visualization:
    with st.expander("🎨 Latest Visualization", expanded=False):
        st.info(f"Saved to: {st.session_state.last_visualization}")
        try:
            st.image(st.session_state.last_visualization)
        except:
            st.warning("Could not load image. Check the path above.")

# Chat input
col1, col2 = st.columns([6, 1])

with col1:
    # Check if we have a prefilled input from example buttons
    if "current_input" in st.session_state and st.session_state.current_input:
        user_input = st.text_input(
            "Your message:",
            value=st.session_state.current_input,
            key="input_box",
            label_visibility="collapsed"
        )
        st.session_state.current_input = ""
    else:
        user_input = st.text_input(
            "Your message:",
            key="input_box",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle message sending
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show loading
    with st.spinner("🤔 Thinking..."):
        # Get response from API
        result = send_message(user_input)
        
        # Add assistant response to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": result.get("response", "No response received")
        })
        
        # Show actions taken if any
        if result.get("actions_taken"):
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📋 Actions: {', '.join(result['actions_taken'])}"
            })
    
    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    🔷 Graph Analysis Agent • Powered by LangGraph & Gemini AI
</div>
""", unsafe_allow_html=True)
