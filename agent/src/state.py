import operator
from langchain_core.messages.utils import AnyMessage
from typing import Annotated, List, Dict, TypedDict

class GraphProperties(TypedDict):
    max_degree: int
    min_degree: int
    avg_degree: float

class GraphAgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    graph: Dict[str, List[str]]
    properties: GraphProperties