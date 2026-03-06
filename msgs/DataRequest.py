from supports.DataStreamType import DataStreamType
from typing import List
from supports.RequestStatus import RequestStatus

class DataRequest:
    def __init__(self, request_type : DataStreamType, total_data_size : int, provided_indexes : List[tuple[int, int]]):
        self.__type = request_type
        self.__indexes = provided_indexes
        self.__size = total_data_size
        self.__status = RequestStatus.PENDING

    def getType(self):
        return self.__type

    def getSize(self):
        return self.__size

    def getStatus(self):
        return self.__status

    def setStatus(self, new_status : RequestStatus):
        self.__status = new_status

    def getDirtyIndexes(self) -> List[tuple[int, int]]:
        return self.__indexes