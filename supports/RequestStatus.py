from enum import Enum

class RequestStatus(Enum):
    PENDING = 0
    BEING_FULFILLED = 1
    DONE = 2