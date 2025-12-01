"""Configuration management for the graph analysis agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    # Gemini API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # LangSmith Configuration
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "graph-analysis-agent")
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Storage Directories
    VISUALIZATION_DIR: Path = Path(os.getenv("VISUALIZATION_DIR", "./visualizations"))
    SOURCES_DIR: Path = Path(os.getenv("SOURCES_DIR", "./sources"))
    
    # Gemini Model Configuration
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_VISION_MODEL: str = "gemini-2.5-flash"
    
    # Graph Visualization Settings
    DEFAULT_GRAPH_LAYOUT: str = "spring"
    DEFAULT_FIGURE_SIZE: tuple[int, int] = (12, 10)
    DEFAULT_NODE_SIZE: int = 500
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Create directories if they don't exist
        cls.VISUALIZATION_DIR.mkdir(parents=True, exist_ok=True)
        cls.SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def setup_langsmith(cls) -> None:
        """Set up LangSmith tracing if enabled."""
        if cls.LANGSMITH_TRACING and cls.LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = cls.LANGSMITH_API_KEY
            os.environ["LANGCHAIN_PROJECT"] = cls.LANGSMITH_PROJECT


# Create config instance
config = Config()
