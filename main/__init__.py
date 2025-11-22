"""
R-Dynamic Graph Coloring API

This module provides a FastAPI application for solving graph coloring problems,
including special cases like antiprism graphs, using various optimization methods.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import router as api_router

# Application configuration
GRAPH_ORDER_START = 3  # T_n
GRAPH_ORDER_END = 3     # T_n
DYNAMIC_COLORING_ORDER = 3  # r
AVAILABLE_COLORS = 8    # k
MAX_GRAPHS = -1         # Maximum number of graphs to process
SAMPLE_GRAPHS = 3       # Number of sample graphs to generate
OUTPUT_DIRECTORY = "../graphs/batches"

def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="R-Dynamic Graph Coloring API",
        description="API for solving graph coloring problems with r-dynamic constraints",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
