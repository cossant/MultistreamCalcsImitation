class LockHandler:
    def __init__(self, managed_data_size : int):
        self.__locks : list[None | str]= [None for _ in range(managed_data_size)]

    def __diapasons_iterator(self, memory_indexes : list[tuple[int, int]]):
        for start, end in memory_indexes:
            for mem_id in range(start, end + 1):
                yield mem_id

    def lock(self, owner : str, memory_indexes : list[tuple[int, int]]):
        if self.is_locked(memory_indexes):
            raise RuntimeError("Trying to lock already locked mem indexes")
        for mem_id in self.__diapasons_iterator(memory_indexes):
            self.__locks[mem_id] = owner

    def unlock(self, unlocker : str, memory_indexes : list[tuple[int, int]]):
        if not self.is_locked(memory_indexes, locked_with=unlocker):
            raise RuntimeError("Trying to unlock mutex which was locked by distinct owner")
        for mem_id in self.__diapasons_iterator(memory_indexes):
            self.__locks[mem_id] = None

    def is_locked(self, memory_indexes : list[tuple[int, int]], locked_with : str = None):
        if locked_with is None:
            return any(self.__locks[mem_id] is not None for mem_id in self.__diapasons_iterator(memory_indexes))
        else:
            return all(self.__locks[mem_id] == locked_with for mem_id in self.__diapasons_iterator(memory_indexes))