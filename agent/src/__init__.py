from fastapi.exceptions import HTTPException
from langchain_core.messages.human import HumanMessage
from agent import GRAPH_AGENT
from typing import List
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from os import getenv

app = FastAPI(
    title="R-Dynamic Graph Coloring Agent",
    description="Agent for solving graph coloring problems with r-dynamic constraints",
    version="1.0.0"
)

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != getenv("C_AGENT_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

@app.get("/health")
def health():
    return {"status": "ok"}

class InvokeParameters(BaseModel):
    prompt: str
    graph: Dict[str, List[str]]

@app.post("/invoke", dependencies=[Security(get_api_key)])
def invoke(params: InvokeParameters):
    messages = [
        HumanMessage(content="\\nothink "+params.prompt)
    ]

    messages = GRAPH_AGENT.invoke({"messages": messages, "graph": params.graph})

    agent_answer = messages["messages"][-1].content
    agent_answer: str = agent_answer.split("</think>")[-1].strip()

    return {"answer": agent_answer}