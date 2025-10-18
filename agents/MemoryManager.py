from storages.Memory import Memory

class MemoryManager:
    def __init__(self, targeted_memory : Memory):
        self.__data_storage = targeted_memory
        self.__access_blockage = [None for _ in range(targeted_memory.getSize())]

#TODO: Implement data lock applying from outer access by ExecutionManager