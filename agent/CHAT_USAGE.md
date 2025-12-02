# Chat Interface Guide

The Graph Analysis Agent now supports conversational chat interactions! You can interact with the agent naturally through text, and it will automatically understand your intent and perform the appropriate actions.

## Features

✅ **Natural Language Understanding**: Ask questions in plain English  
✅ **Automatic Graph Detection**: Paste graphs directly in the chat  
✅ **Multi-turn Conversations**: The agent remembers context  
✅ **Action Detection**: Automatically generates visualizations or analysis when requested  
✅ **Session Management**: Each conversation maintains its own state  

## Using the Chat Interface

### Option 1: Streamlit Interface (Recommended)

1. **Start the API server**:
   ```bash
   cd agent
   uv run uvicorn api.main:app --reload
   ```

2. **Start the Streamlit app** (in a new terminal):
   ```bash
   cd agent
   uv run streamlit run streamlit_app.py
   ```

3. **Start chatting!**
   - Streamlit will automatically open in your browser (usually http://localhost:8501)
   - Use the sidebar for examples and session info
   - Type messages in the input box
   - See visualizations and analysis results inline

### Option 2: Terminal Interface

1. **Start the API server** (if not already running):
   ```bash
   uv run uvicorn api.main:app --reload
   ```

2. **Run the CLI chat**:
   ```bash
   uv run python chat_cli.py
   ```

3. **Use commands**:
   - `/help` - Show help and examples
   - `/history` - View conversation history
   - `/clear` - Clear the current session
   - `/quit` - Exit the chat

### Option 3: API Endpoint

Send POST requests to `/chat/message`:

```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is a chromatic number?",
    "session_id": "my-session"
  }'
```

## Example Conversations

### Example 1: Learning About Graph Theory

```
You: What is a chromatic number?

Agent: The chromatic number of a graph is the minimum number of colors 
needed to color all vertices such that no two adjacent vertices share 
the same color. It's a fundamental concept in graph coloring theory...
```

### Example 2: Loading and Analyzing a Graph

```
You: {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}

Agent: I've loaded your graph! It has 3 nodes and 3 edges. 
What would you like to know about it?

You: Is this graph bipartite?

Agent: No, this graph is not bipartite. A bipartite graph cannot 
contain odd-length cycles, and your graph forms a triangle (3-cycle), 
which is odd. Therefore, it cannot be colored with just 2 colors.

You: Analyze the graph

Agent: I've analyzed your graph! Here are the key properties:

📊 **Basic Properties:**
- Nodes: 3
- Edges: 3
- Connected: True
- Density: 1.0
- Is tree: False
- Is bipartite: False

🎨 **Chromatic Number:**
- Estimated: 3
- Upper bound: 3

What else would you like to know?
```

### Example 3: Requesting Visualization

```
You: [[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]]

Agent: I've loaded your graph! It has 4 nodes and 5 edges. 
What would you like to know about it?

You: Show me a visualization

Agent: I've created a visualization of your graph! 
You can access it at: visualizations/graph_20231201_215530.png
```

## What the Chat Can Do

### Automatic Detection

The chat endpoint automatically detects:

1. **Graph Input**: JSON format adjacency lists or matrices
2. **Visualization Requests**: Keywords like "visualize", "show", "draw"
3. **Analysis Requests**: Keywords like "analyze", "properties", "chromatic"
4. **General Questions**: Everything else goes to Gemini for Q&A

### Supported Actions

- **Load graphs** from adjacency lists or matrices
- **Answer questions** about graph theory concepts
- **Generate visualizations** of loaded graphs
- **Perform analysis** (chromatic number, centrality, connectivity)
- **Maintain context** across multiple messages in a session

## API Endpoint Details

### POST /chat/message

Send a chat message to the agent.

**Request:**
```json
{
  "message": "What is a chromatic number?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "The chromatic number is...",
  "session_id": "optional-session-id",
  "actions_taken": ["Answered question using Gemini"],
  "visualization_path": null,
  "analysis_results": null,
  "conversation_history": [...]
}
```

### GET /chat/history/{session_id}

Retrieve conversation history for a session.

### DELETE /chat/session/{session_id}

Clear a session and start fresh.

## Tips for Best Results

1. **Be specific**: "Analyze this graph" works better than just "analyze"
2. **Use proper JSON format**: For graph input, ensure valid JSON syntax
3. **Ask follow-up questions**: The agent remembers your graph across messages
4. **Try examples**: Use the example buttons in the web interface to get started

## Integration with Chat Platforms

The `/chat/message` endpoint can be easily integrated with:

- Slack bots
- Discord bots  
- Telegram bots
- Custom chat applications
- Webhooks

Simply POST user messages to the endpoint and display the `response` field.

## Troubleshooting

**"Cannot connect to API server"**
- Make sure the server is running: `uv run uvicorn api.main:app --reload`
- Check that it's accessible at `http://localhost:8000`

**"Graph loading failed"**
- Ensure JSON format is valid (use quotes around strings)
- Try simpler graphs first to test
- Check the conversation history for error messages

**Web interface not working**
- Enable CORS in your browser if testing locally
- Check browser console for errors
- Verify API_URL in the HTML file matches your server

## Advanced: Custom Integration

To integrate with your own chat platform:

```python
import requests

def send_to_agent(user_message, session_id):
    response = requests.post(
        "http://localhost:8000/chat/message",
        json={
            "message": user_message,
            "session_id": session_id
        }
    )
    return response.json()["response"]

# Use in your bot
user_msg = "What is a chromatic number?"
bot_response = send_to_agent(user_msg, "user-123")
print(bot_response)
```

Happy chatting! 🔷
