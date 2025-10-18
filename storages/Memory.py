from typing import List

class Memory:
    def __init__(self, mem_size : int):
        self.__data = [None] * mem_size

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data[item]