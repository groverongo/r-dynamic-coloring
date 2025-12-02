# Graph Analysis Agent

A powerful LangGraph-based agent for graph theory analysis, powered by Google's Gemini AI, NetworkX, and FastAPI.

## Features

- **Multiple Input Formats**: Accept graphs as adjacency lists, adjacency matrices, or images
- **Intelligent Q&A**: Ask questions about graph properties using natural language
- **Visual Analysis**: Generate beautiful graph visualizations with customizable layouts
- **Coloring Support**: Apply and validate node/edge colorings
- **Comprehensive Analysis**: Compute chromatic numbers, centrality measures, connectivity, and more
- **Image Understanding**: Extract graph structure from images using Gemini Vision
- **REST API**: Full-featured FastAPI application for integration
- **Session Management**: Maintain separate graph states for multiple users
- **Knowledge Sources**: Upload custom documents for specialized graph theory learning
- **💬 Chat Interface**: Conversational interface for natural interactions

## Chat Interface 💬

The agent now supports **conversational chat interactions**! Interact naturally through text and the agent will automatically understand your intent.

### Quick Start with Chat

**Option 1: Streamlit Interface (Recommended)**

```bash
# Terminal 1: Start the API server
uv run uvicorn api.main:app --reload

# Terminal 2: Start Streamlit
uv run streamlit run streamlit_app.py
```

The Streamlit app will open in your browser with:
- Beautiful gradient UI
- Real-time chat with the agent
- Example buttons for quick testing
- Visualization display in the interface
- Session management

**Option 2: Terminal Chat**

```bash
uv run python chat_cli.py
```

### What You Can Do in Chat

- **Ask questions**: "What is a chromatic number?"
- **Load graphs**: Paste JSON like `{"A": ["B"], "B": ["A"]}`
- **Request visualizations**: "Show me the graph"
- **Get analysis**: "Analyze this graph"
- **Multi-turn conversations**: The agent remembers context

See [CHAT_USAGE.md](CHAT_USAGE.md) for detailed chat documentation.

## Architecture

This agent uses **LangGraph** for workflow orchestration with the following nodes:

1. **Input Processing**: Parses graphs from various formats
2. **Coloring Processing**: Applies and validates colorings
3. **Request Router**: Intelligently routes queries to appropriate handlers
4. **Visualization Generator**: Creates graph images with NetworkX
5. **Question Answering**: Uses Gemini for natural language Q&A
6. **Graph Analyzer**: Computes graph properties and metrics

## Prerequisites

- Python 3.11 or higher
- UV package manager
- Google Gemini API key

## Installation

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Navigate to the agent directory**:
```bash
cd agent
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Configuration

Edit the `.env` file:

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional - LangSmith Tracing
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=graph-analysis-agent
LANGSMITH_TRACING=false

# API Server
HOST=0.0.0.0
PORT=8000

# Storage
VISUALIZATION_DIR=./visualizations
SOURCES_DIR=./sources
```

## Quick Start

### Start the API Server

```bash
uv run uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

### Programmatic Usage

```python
from agent.graph import run_agent

# Load a graph from adjacency list
result = run_agent(
    graph_input={"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]},
    input_format="adjacency_list",
    session_id="my_session"
)

# Ask a question
result = run_agent(
    user_input="What is the chromatic number of this graph?",
    session_id="my_session"
)

print(result["messages"][-1]["content"])
```

## API Usage Examples

### 1. Load a Graph (Adjacency List)

```bash
curl -X POST "http://localhost:8000/graph/adjacency-list" \
  -H "Content-Type: application/json" \
  -d '{
    "adjacency_list": {
      "A": ["B", "C"],
      "B": ["A", "C"],
      "C": ["A", "B"]
    },
    "session_id": "session_1"
  }'
```

### 2. Load a Graph (Adjacency Matrix)

```bash
curl -X POST "http://localhost:8000/graph/adjacency-matrix" \
  -H "Content-Type: application/json" \
  -d '{
    "adjacency_matrix": [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
    "node_labels": ["A", "B", "C"],
    "session_id": "session_1"
  }'
```

### 3. Upload Graph Image

```bash
curl -X POST "http://localhost:8000/graph/image" \
  -F "file=@graph.png" \
  -F "session_id=session_1"
```

### 4. Set a Coloring

```bash
curl -X POST "http://localhost:8000/query/coloring" \
  -H "Content-Type: application/json" \
  -d '{
    "coloring": {"A": "red", "B": "blue", "C": "red"},
    "session_id": "session_1"
  }'
```

### 5. Ask a Question

```bash
curl -X POST "http://localhost:8000/query/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Is this graph bipartite?",
    "session_id": "session_1"
  }'
```

### 6. Generate Visualization

```bash
curl -X POST "http://localhost:8000/query/visualize" \
  -H "Content-Type: application/json" \
  -d '{
    "layout": "circular",
    "title": "My Graph",
    "session_id": "session_1"
  }'
```

Retrieve the visualization:
```bash
curl "http://localhost:8000/query/visualize/session_1" --output graph.png
```

### 7. Analyze Graph

```bash
curl -X POST "http://localhost:8000/query/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "comprehensive",
    "session_id": "session_1"
  }'
```

### 8. Upload Learning Sources

```bash
curl -X POST "http://localhost:8000/sources/upload" \
  -F "file=@graph_theory_notes.pdf" \
  -F "description=My graph theory reference"
```

## Python Client Examples

See `examples/` directory for detailed Python examples:

- `basic_usage.py`: Basic graph operations
- `api_examples.py`: API client usage with requests library

## Project Structure

```
agent/
├── agent/              # LangGraph agent implementation
│   ├── __init__.py
│   ├── graph.py       # Workflow definition
│   ├── nodes.py       # Node implementations
│   └── prompts.py     # LLM prompts
├── api/               # FastAPI application
│   ├── __init__.py
│   ├── main.py        # FastAPI app
│   ├── schemas.py     # Pydantic models
│   └── routers/       # API endpoints
│       ├── graph.py   # Graph input endpoints
│       ├── query.py   # Query/visualization endpoints
│       └── sources.py # Learning sources
├── tools/             # Graph analysis tools
│   ├── __init__.py
│   ├── graph_analysis.py
│   ├── graph_visualization.py
│   └── image_parsing.py
├── tests/             # Test suite
├── examples/          # Usage examples
├── config.py          # Configuration
├── state.py           # LangGraph state schema
├── graph_parsers.py   # Input parsers
└── pyproject.toml     # UV project config
```

## Supported Graph Analysis

- **Basic Properties**: nodes, edges, density, connectivity
- **Degree Analysis**: degree sequence, min/max/avg degree, regularity
- **Centrality Measures**: degree, betweenness, closeness, eigenvector
- **Chromatic Number**: Estimation with greedy coloring and bounds
- **Clique Detection**: Find maximum cliques
- **Path Finding**: Shortest paths, all shortest paths
- **Connectivity**: Connected components, node/edge connectivity
- **Cycle Detection**: Find cycles in the graph

## Supported Layouts

- `spring`: Force-directed layout (default)
- `circular`: Nodes arranged in a circle
- `kamada_kawai`: Force-directed with better edge lengths
- `planar`: Planar embedding (if graph is planar)
- `shell`: Concentric circles
- `spectral`: Based on graph spectrum

## Development

### Run Tests

```bash
uv run pytest tests/
```

### Code Formatting

```bash
uv run black .
uv run ruff check .
```

## LangSmith Tracing

To enable LangSmith tracing for debugging:

1. Get your LangSmith API key from https://smith.langchain.com
2. Set environment variables in `.env`:
   ```
   LANGSMITH_API_KEY=your_key
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=graph-analysis-agent
   ```

## Troubleshooting

**"GOOGLE_API_KEY environment variable is required"**
- Make sure you've created a `.env` file and added your Gemini API key

**"Failed to parse graph from image"**
- Ensure the image is clear and graph structure is visible
- Try with a simpler graph first
- Check that your Gemini API key has access to vision models

**"Session not found"**
- Make sure you're using the same `session_id` across requests
- Sessions are stored in memory and reset when the server restarts

## Future Enhancements

- [ ] Persistent session storage (Redis/Database)
- [ ] Advanced RAG for learning sources
- [ ] Graph editing operations (add/remove nodes/edges)
- [ ] Export graphs to various formats (GraphML, GEXF, etc.)
- [ ] Batch processing of multiple graphs
- [ ] WebSocket support for real-time updates
- [ ] Docker containerization
- [ ] Graph algorithms (MST, max flow, matching, etc.)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
