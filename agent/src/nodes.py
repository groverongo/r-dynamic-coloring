import json
from models import GROQ_MODEL
from messages.system import PROPERTIES_INSTRUCTION, PROFESSOR_INSTRUCTION
from state import GraphAgentState, GraphProperties

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
    
    ai_msg = GROQ_MODEL.invoke(
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