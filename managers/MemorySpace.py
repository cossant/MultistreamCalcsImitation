from storages.Memory import Memory
from managers.LockHandler import LockHandler
class MemorySpace:
    def __init__(self, mem_size : int):
        self._memory = Memory(mem_size)
        self._mutex_manager = LockHandler(managed_data_size=mem_size)

    def __len__(self):
        return self._memory.getSize()

    # Returning None if memory is not allocated, or mem_diapasons if successfully
    def request_memory(self, requested_memory_size : int, requester_name : str):
        if requested_memory_size > len(self) or self._mutex_manager.countUnlocked() < requested_memory_size:
            return None
        else:
            allocated_diapasons = self.__construct_free_diapasons(requested_memory_size)
            self._mutex_manager.lock(requester_name, allocated_diapasons)
            return allocated_diapasons

    def  getFreeSpaceCount(self):
        return self._mutex_manager.countUnlocked()

    def free_memory(self, owner_name : str, memory_indexes : list[tuple[int, int]]):
        self._mutex_manager.unlock(owner_name, memory_indexes)

    def lock_memory(self, memory_indexes : list[tuple[int, int]], locker_name):
        self._mutex_manager.lock(locker_name, memory_indexes)

    def isLocked(self, memory_indexes : list[tuple[int, int]]):
        self._mutex_manager.is_locked_span(memory_indexes)

    # first-fit scatter allocation
    # Yes, memory WILL get more fragmentated in time
    # This can be managed by adding defragmentation algorithm, or implementing "allocate from largest ranges first"
    # Though, I am not doing this right now - might be refactored later
    def __construct_free_diapasons(self, requested_length = None):
        if requested_length is None:
            requested_length = len(self)
        diapason_sequence = []
        sequence_length = 0
        diapason_start, diapason_end = None, None
        for index in range(len(self)):
            if not self._mutex_manager.is_locked(index):
                if diapason_start is None:
                    diapason_start = index
                sequence_length += 1
                if sequence_length == requested_length:
                    diapason_end = index
            elif diapason_start is not None:
                diapason_end = index - 1
            if diapason_end is not None:
                diapason_sequence.append(tuple([diapason_start, diapason_end]))
                diapason_start, diapason_end = None, None
            if sequence_length == requested_length:
                break
        return diapason_sequence



