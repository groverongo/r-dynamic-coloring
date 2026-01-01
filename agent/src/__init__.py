from langchain_core.messages.human import HumanMessage
from agent import GRAPH_AGENT
from typing import List
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="R-Dynamic Graph Coloring Agent",
    description="Agent for solving graph coloring problems with r-dynamic constraints",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

class InvokeParameters(BaseModel):
    prompt: str
    graph: Dict[str, List[str]]

@app.post("/invoke")
def invoke(params: InvokeParameters):
    messages = [
        HumanMessage(content="\\nothink "+params.prompt)
    ]

    messages = GRAPH_AGENT.invoke({"messages": messages, "graph": params.graph})
    for m in messages["messages"]:
        m.pretty_print()

    return messages