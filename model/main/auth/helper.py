from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from fastapi import Security, status
from os import getenv

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != getenv("C_MODEL_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

AUTH_DEPENDENCIES = [Security(get_api_key)]