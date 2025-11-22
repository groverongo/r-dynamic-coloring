from pulp import LpProblem, LpVariable
from enum import Enum
import numpy.typing as npt
import numpy as np
from dataclasses import dataclass

class MODEL_METHOD(Enum):
    ACR = 'ACR'
    ACR_H = 'ACR-H'
    ACR_R = 'ACR-R'
    ACR_RH = 'ACR-RH'

@dataclass
class Coloring_Solution:
    model: LpProblem
    w: npt.NDArray[LpVariable]
    x: npt.NDArray[npt.NDArray[LpVariable]]
    q: npt.NDArray[npt.NDArray[LpVariable]]