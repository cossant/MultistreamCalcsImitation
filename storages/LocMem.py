import Memory
# TODO: Implement MemoryManager usage
class LocMem(Memory.Memory):
    def __init__(self, mem_size : int):
        super().__init__(mem_size)
        self.__free_position = [True for _ in range(mem_size)]

    def getFreeSpace(self):
        free_positions = 0
        for index in range(self._size):
            if self.__free_position[index]:
                free_positions += 1
        return free_positions

    def allocateMemory(self, desired_size : int):
        if self.getFreeSpace() < desired_size:
            raise MemoryError("Trying to allocate more memory than accessible")
        dirty_indexes = []
        indexes_found = 0
        for curr_memory_position in range(self._size):
            if self.__free_position[curr_memory_position]:
                indexes_found += 1
                dirty_indexes.append(curr_memory_position)
                self.__free_position[curr_memory_position] = False
            if indexes_found == desired_size:
                break
        return self._clearMemoryRanges(dirty_indexes)

    def _clearMemoryRanges(self, dirty_indexes):
        clear_indexes = []
        current_interval = None
        for index_id in range(len(dirty_indexes)):
            # TODO: WIP - Make from 12356789 -> [1,3], [5,5], [6,9]
            if current_interval is None:
                current_interval = [dirty_indexes[index_id]]
            else:
                if index
