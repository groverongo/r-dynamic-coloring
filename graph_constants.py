
from typing import Callable, Tuple
from enum import Enum

MANHATTAN_DISTANCE: Callable[[Tuple[int, int], Tuple[int, int]], int] = lambda tuple_1, tuple_2: abs(tuple_1[0] - tuple_2[0]) + abs(tuple_1[1] - tuple_2[1])
X_DIFFERENCE: Callable[[Tuple[int, int], Tuple[int, int]], int] = lambda tuple_1, tuple_2: tuple_1[0] - tuple_2[0]
Y_DIFFERENCE: Callable[[Tuple[int, int], Tuple[int, int]], int] = lambda tuple_1, tuple_2: tuple_1[1] - tuple_2[1]

CONDITION_1: Callable[[Tuple[int, int], Tuple[int, int]], bool] = lambda tuple_1, tuple_2: MANHATTAN_DISTANCE(tuple_1, tuple_2) == 1
CONDITION_2: Callable[[Tuple[int, int], Tuple[int, int]], bool] = lambda tuple_1, tuple_2: MANHATTAN_DISTANCE(tuple_1, tuple_2) == 2 and X_DIFFERENCE(tuple_1, tuple_2) != Y_DIFFERENCE(tuple_1, tuple_2) and abs(Y_DIFFERENCE(tuple_1, tuple_2)) == abs(X_DIFFERENCE(tuple_1, tuple_2)) == 1
EDGE_CONDITION: Callable[[Tuple[int, int], Tuple[int, int]], bool] = lambda tuple_1, tuple_2: CONDITION_1(tuple_1, tuple_2) or CONDITION_2(tuple_1, tuple_2)

class MODEL_METHOD(Enum):
    ACR = 'ACR'
    ACR_H = 'ACR-H'
    ACR_R = 'ACR-R'
    ACR_RH = 'ACR-RH'

AVAILABLE_COLORS = ["#FFC0CB", "#90EE90", "#ADD8E6", "#FFFFE0", "#E6E6FA", "#FFD700", "#F0E68C", "#98FB98", "#F5DEB3", "#B0E0E6"]