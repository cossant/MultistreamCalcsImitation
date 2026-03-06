from agents.AgentInterface import AgentInterface
from supports.GLOBAL_CONSTANTS import DATA_TRANSACTION_MAX_SIZE
from storages.Memory import Memory
from typing import List

class DataTransferStream(AgentInterface):
    def __init__(self,
                 origin : Memory,
                 work_indexes_origin : List[tuple[int, int]],
                 destination : Memory,
                 work_indexes_destination : List[tuple[int, int]]
                 ):
        self.__max_batch_size = DATA_TRANSACTION_MAX_SIZE
        self.__origin = origin
        self.__destination = destination
        self.__origin_indexes_dirty = work_indexes_origin
        self.__destination_indexes_dirty = work_indexes_destination
        self.__data_length = self.__calculateDataLength()
        self.__data_moved = 0
        self.__origin_indexes = self._clearIndexes(self.__origin_indexes_dirty)
        self.__destination_indexes = self._clearIndexes(self.__destination_indexes_dirty)

    def tick(self, sim):


    def getOriginIndexes(self):
        return self.__origin_indexes_dirty

    def getDestinationIndexes(self):
        return self.__destination_indexes_dirty

    def _clearIndexes(self, indexes_tuples : List[tuple[int, int]]) -> List[int]:
        clear_indexes = []
        for interval in indexes_tuples:
            for index in range(*interval):
                clear_indexes.append(index)
        return clear_indexes

    def __calculateDataLength(self) -> int:
        # Asserting that in and out indexes are set
        if self.__origin_indexes is None or self.__destination_indexes is None:
            raise RuntimeError("E: Trying to use a datastream without origin/destination indexes defined")
        # Asserting equality in work fields sizes
        origin_data_len = 0
        for interval in reversed(self.__origin_indexes):
            origin_data_len += interval[1] - interval[0]
        destination_data_len = 0
        for interval in reversed(self.__destination_indexes):
            destination_data_len += interval[1] - interval[0]
        if not origin_data_len == destination_data_len:
            raise RuntimeError("E: Data stream origin/destination data sizes doesn't match")
        return origin_data_len

    def transferBatch(self):
        transferred_data_size = self.__data_length - self.__data_moved
        this_batch_size = self.__max_batch_size if transferred_data_size > self.__max_batch_size else transferred_data_size
        sender = self.__origin
        receiver = self.__destination
        for i in range(this_batch_size):
            real_sender_index = self.__origin_indexes[self.__data_moved] + i
            real_receiver_index = self.__destination_indexes[self.__data_moved] + i
            receiver[real_receiver_index] = sender[real_sender_index]
        self.__data_moved += this_batch_size
        return self.__data_moved == self.__data_length





