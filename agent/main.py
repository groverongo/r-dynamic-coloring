from messages.system import PROPERTIES_INSTRUCTION
from typing import TypedDict
from typing import List
from typing import Dict
from langchain_core.messages.utils import AnyMessage
from typing import Annotated
from messages.system import PROFESSOR_INSTRUCTION
from langchain_core.messages.human import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import json, operator
from langgraph.graph import StateGraph, START, END
from langchain_core.messages.system import SystemMessage

class GraphProperties(TypedDict):
    max_degree: int
    min_degree: int
    avg_degree: float

class GraphAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    graph: Dict[str, List[str]]
    properties: GraphProperties



model = ChatGroq(
    model="qwen/qwen3-32b",
    reasoning_effort=None,
    max_tokens=200,
)

def graph_properties(state: GraphAgentState) -> GraphAgentState:

    degrees = [len(state["graph"][node]) for node in state["graph"]]

    properties: GraphProperties = {
        "max_degree": max(degrees),
        "min_degree": min(degrees),
        "avg_degree": sum(degrees) / len(degrees)
    }

    return {
        "messages": [],
        "graph": state["graph"], 
        "properties": properties
    }

def professor_interaction(state: GraphAgentState) -> GraphAgentState:

    properties_str = '\n'.join([f'- {k}: {v}' for k, v in state['properties'].items()])
    
    ai_msg = model.invoke(
        [
            PROFESSOR_INSTRUCTION.format(graph=json.dumps(state['graph'])), 
            PROPERTIES_INSTRUCTION.format(properties=properties_str)
        ]
        + state["messages"]
    )

    return {
        "messages": [ai_msg],
        "graph": state["graph"],
        "properties": state["properties"]
    }

agent_builder = StateGraph(GraphAgentState)

agent_builder.add_node("graph_properties", graph_properties)
agent_builder.add_node("professor_interaction", professor_interaction)

agent_builder.add_edge(START, "graph_properties")
agent_builder.add_edge("graph_properties", "professor_interaction")
agent_builder.add_edge("professor_interaction", END)

agent = agent_builder.compile()

messages = [
    HumanMessage(content="What can you tell me about this graph?")
]

messages = agent.invoke({"messages": messages, "graph": {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}})
for m in messages["messages"]:
    m.pretty_print()


