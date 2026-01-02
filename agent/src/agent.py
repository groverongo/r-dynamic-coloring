from nodes import graph_properties, professor_interaction
from state import GraphAgentState
from langchain_core.messages.human import HumanMessage
from langgraph.graph import StateGraph, START, END


GRAPH_AGENT_BUILDER = StateGraph(GraphAgentState)

GRAPH_AGENT_BUILDER.add_node("graph_properties", graph_properties)
GRAPH_AGENT_BUILDER.add_node("professor_interaction", professor_interaction)

GRAPH_AGENT_BUILDER.add_edge(START, "graph_properties")
GRAPH_AGENT_BUILDER.add_edge("graph_properties", "professor_interaction")
GRAPH_AGENT_BUILDER.add_edge("professor_interaction", END)

GRAPH_AGENT = GRAPH_AGENT_BUILDER.compile()

if __name__ == "__main__":
    messages = [
        HumanMessage(content="What can you tell me about this graph?")
    ]

    messages = GRAPH_AGENT.invoke({"messages": messages, "graph": {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}})
    for m in messages["messages"]:
        m.pretty_print()