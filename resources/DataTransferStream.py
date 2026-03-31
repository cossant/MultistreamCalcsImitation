from managers.MemorySpace import MemorySpace
from assets.CompletionStatus import CompletionStatus
from assets.GLOBAL_CONSTANTS import DATA_TRANSACTION_MAX_SIZE
from typing import List
import deal


class DataTransferStream:
    def __init__(self,
                 origin : MemorySpace,
                 work_indexes_origin : List[tuple[int, int]],
                 destination : MemorySpace,
                 work_indexes_destination : List[tuple[int, int]]
                 ):
        self.__max_batch_size = DATA_TRANSACTION_MAX_SIZE
        self.__origin = origin
        self.__destination = destination
        self.__origin_intervals = work_indexes_origin
        self.__destination_intervals = work_indexes_destination
        self.__data_moved = 0
        self.__origin_indexes = self.__generateIndexses(self.__origin_intervals)
        self.__destination_indexes = self.__generateIndexses(self.__destination_intervals)
        self.__data_length = self.__calculateDataLength()
        self.__status = CompletionStatus.IN_PROGRESS

    def getOriginIndexes(self):
        return self.__origin_indexes

    def getDestinationIndexes(self):
        return self.__destination_indexes

    def getMovedElementsCount(self):
        return self.__data_moved

    def isCompleted(self):
        return self.__status == CompletionStatus.DONE

    def getTotalElementsCount(self):
        return self.__data_length

    def __generateIndexses(self, interval_tuples: List[tuple[int, int]]) -> List[int]:
        indexes = []
        for interval in interval_tuples:
            for index in range(interval[0], interval[1] + 1):
                indexes.append(index)
        return indexes

    # def _get_origin_data_length(self) -> int:
    #     total = 0
    #     for interval in reversed(self.__origin_intervals):
    #         total += interval[1] + 1 - interval[0]
    #     return total

    def __get_destination_data_length(self) -> int:
        total = 0
        for interval in reversed(self.__destination_intervals):
            total += interval[1] + 1 - interval[0]
        return total

    @deal.pre(lambda self: self.__origin_indexes is not None and self.__destination_indexes is not None, 
              message="E: Trying to use a datastream without origin/destination indexes defined")
    @deal.ensure(lambda self, result: result == self.__get_destination_data_length(), 
              message="E: Data stream origin/destination data sizes doesn't match")
    def __calculateDataLength(self) -> int:
        origin_data_len = 0
        for interval in reversed(self.__origin_intervals):
            origin_data_len += interval[1] + 1 - interval[0]
        # destination_data_len = 0
        # for interval in reversed(self.__destination_intervals):
        #     destination_data_len += interval[1] + 1 - interval[0]

        return origin_data_len

    @deal.pre(lambda self: self.__data_length - self.__data_moved != 0, message="E: DataStream attempt to transfer more data, than there is")
    def transferBatch(self):
        untransferred_data_size = self.__data_length - self.__data_moved
        this_batch_size = self.__max_batch_size if untransferred_data_size > self.__max_batch_size else untransferred_data_size
        sender = self.__origin
        receiver = self.__destination
        for i in range(0, this_batch_size):
            sender_index = self.__origin_indexes[self.__data_moved + i]
            receiver_index = self.__destination_indexes[self.__data_moved + i]
            receiver.imitateWrite(receiver_index, sender.imitateRead(sender_index))
        self.__data_moved += this_batch_size
        if self.__data_moved == self.__data_length:
            self.__status = CompletionStatus.DONE
        return self.__data_moved == self.__data_length





