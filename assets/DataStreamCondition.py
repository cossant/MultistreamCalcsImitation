from enum import Enum
class DataStreamCondition(Enum):
    PUSHING = 0
    PULLING = 1
    AWAITING = 2