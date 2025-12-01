"""Knowledge source management API endpoints."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
import shutil
from typing import List
import uuid

from api.schemas import SourceUploadResponse
from config import config

router = APIRouter(prefix="/sources", tags=["sources"])

# In-memory source registry (replace with database in production)
sources_registry = {}


@router.post("/upload", response_model=SourceUploadResponse)
async def upload_source(file: UploadFile = File(...), description: str = ""):
    """Upload a learning source document."""
    try:
        # Generate unique ID
        source_id = str(uuid.uuid4())
        
        # Save file
        file_path = config.SOURCES_DIR / f"{source_id}_{file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Register source
        sources_registry[source_id] = {
            "id": source_id,
            "filename": file.filename,
            "path": str(file_path),
            "description": description,
        }
        
        return SourceUploadResponse(
            success=True,
            message=f"Source '{file.filename}' uploaded successfully",
            source_id=source_id,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_sources():
    """List all available learning sources."""
    return {
        "sources": list(sources_registry.values()),
        "count": len(sources_registry),
    }


@router.delete("/{source_id}", response_model=SourceUploadResponse)
async def delete_source(source_id: str):
    """Delete a learning source."""
    if source_id not in sources_registry:
        raise HTTPException(status_code=404, detail="Source not found")
    
    try:
        source = sources_registry[source_id]
        file_path = Path(source["path"])
        
        if file_path.exists():
            file_path.unlink()
        
        del sources_registry[source_id]
        
        return SourceUploadResponse(
            success=True,
            message=f"Source '{source['filename']}' deleted successfully",
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{source_id}")
async def get_source_info(source_id: str):
    """Get information about a specific source."""
    if source_id not in sources_registry:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return sources_registry[source_id]
