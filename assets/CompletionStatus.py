from enum import Enum

class CompletionStatus(Enum):
    PENDING = 0
    ASSIGNED = 1
    IN_PROGRESS = 2
    DONE = 3