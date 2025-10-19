from typing import List

class Memory:
    def __init__(self, mem_size : int):
        self.__data = [1 for  _ in range(mem_size)] # Really important data
        self._size = mem_size

    def __setitem__(self, key, value):
        if not self._indexIsViable(key):
            raise IndexError("Data index is OOB")
        self.__data[key] = value

    def __getitem__(self, item):
        if not self._indexIsViable(item):
            raise IndexError("Data index is OOB")
        return self.__data[item]

    def getSize(self):
        return  self._size

    def _indexIsViable(self, index):
        if index < 0 or index >  (self._size - 1):
            return False
        else:
            return True