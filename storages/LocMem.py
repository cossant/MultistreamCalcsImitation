import Memory
# TODO: Implement MemoryManager usage
class LocMem(Memory.Memory):
    def allocateMemory(self, desired_size : int):
        # TODO: Look for unused spaces in existing mem
        # TODO: Think over idea of a transactions, which notice opener and closer of a mem position