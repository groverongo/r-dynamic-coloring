from enum import Enum
from typing import Set, Tuple

Star_Triad_Type = Tuple[int, int, int]
Border_Type = Set[int]

class INDEX_ACCESS_TRIAD(Enum):
    VERTEX_1 = 0
    MIDDLE = 1
    VERTEX_2 = 2