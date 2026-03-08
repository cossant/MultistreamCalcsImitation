from storages.Memory import Memory
from managers.LockHandler import LockHandler
class MemorySpace:
    def __init__(self, mem_size : int):
        self._memory = Memory(mem_size)
        self._mutex_manager = LockHandler(managed_data_size=mem_size)

    def request_memory(self, requested_memory_size : int, requester_name : str):
        # should be
        # 1. Checking if requested memory size is possible
        # 2. Checking if it is free (decompose to separate function)
        # 3. Returning None if memory is not allocated, or mem_diapasons if successfull
        # TODO: Implement memory checking and allocation
