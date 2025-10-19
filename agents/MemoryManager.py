from storages.Memory import Memory

class MemoryManager:
    def __init__(self, targeted_memory : Memory):
        self.__data_storage = targeted_memory
        self.__access_blockage = [None for _ in range(targeted_memory.getSize())]

    def applyLock(self, index_ranges, locking_task):
        for span in index_ranges:
            for index in span:
                if self.__access_blockage[index] is not None:
                    raise MemoryError("Trying to lock already locked memory position")
                else:
                    self.__access_blockage[index] = locking_task

    def dropLock(self, index_ranges, unlocking_task, overrule = False):
        for span in index_ranges:
            for index in span:
                if (self.__access_blockage[index] == unlocking_task) or overrule:
                    self.__access_blockage[index] = None
                else:
                    raise MemoryError("Not owner task trying to unlock memory position without overrule")
    def readPos(self, index, reading_task):
        if self.__access_blockage[index] == reading_task:
            return self.__data_storage[index]
        else:
            raise MemoryError("Trying to read locked  or unclaimed memory")

    def writePos(self, index, writing_task):
        if self.__access_blockage[index] == writing_task:
            self.__data_storage[index] = 1 # Really hard work here
        else:
            raise MemoryError("Trying to read locked  or unclaimed memory")