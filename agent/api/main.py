"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import config
from api.routers import graph, query, sources


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    # Startup
    print("🚀 Starting Graph Analysis Agent API...")
    
    # Validate configuration
    try:
        config.validate()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise
    
    # Setup LangSmith if enabled
    config.setup_langsmith()
    if config.LANGSMITH_TRACING:
        print(f"📊 LangSmith tracing enabled: {config.LANGSMITH_PROJECT}")
    
    print(f"📁 Visualizations directory: {config.VISUALIZATION_DIR}")
    print(f"📁 Sources directory: {config.SOURCES_DIR}")
    print(f"🤖 Gemini model: {config.GEMINI_MODEL}")
    print("✅ Ready to accept requests!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Graph Analysis Agent API...")


# Create FastAPI app
app = FastAPI(
    title="Graph Analysis Agent",
    description="LangGraph-based agent for graph theory analysis with Gemini integration",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(graph.router)
app.include_router(query.router)
app.include_router(sources.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Graph Analysis Agent API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "graph_input": {
                "adjacency_list": "POST /graph/adjacency-list",
                "adjacency_matrix": "POST /graph/adjacency-matrix",
                "image": "POST /graph/image",
                "info": "GET /graph/info/{session_id}",
            },
            "queries": {
                "ask": "POST /query/ask",
                "coloring": "POST /query/coloring",
                "visualize": "POST /query/visualize",
                "get_visualization": "GET /query/visualize/{session_id}",
                "analyze": "POST /query/analyze",
            },
            "sources": {
                "upload": "POST /sources/upload",
                "list": "GET /sources/list",
                "delete": "DELETE /sources/{source_id}",
                "info": "GET /sources/{source_id}",
            },
        },
        "documentation": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "gemini_configured": bool(config.GOOGLE_API_KEY),
        "langsmith_enabled": config.LANGSMITH_TRACING,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
    )
