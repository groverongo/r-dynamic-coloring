from typing import Dict, List, Literal, Tuple, Union, Optional
from pydantic import BaseModel

class BasePlotColoringRequest(BaseModel):
    coloring: Dict[int, int]

class CirculantPlotRequest(BasePlotColoringRequest):
    n: int
    connections: List[int]