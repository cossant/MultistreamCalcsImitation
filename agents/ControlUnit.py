from agents.AgentInterface import AgentInterface
from agents.MemoryManager import MemoryManager
from storages.LocMem import LocMem
from agents.DataTransferStream import DataTransferStream
from msgs.DataRequest import DataRequest, DataStreamType
from supports.RequestStatus import RequestStatus

class ControlUnit(AgentInterface):
    def __init__(self, global_memory : MemoryManager, local_memory : LocMem):
        self.__pending_data_requests = [] # FIFO queue
        self.__data_connection = None
        self._global_mem = global_memory
        self._local_mem = local_memory

    def tick(self, sim):


    def registerDataRequest(self, request : DataRequest):
        self.__pending_data_requests.append(request)

    def tickDataTransfer(self):
        # Trying to pick new request
        if (self.__data_connection is None) and (len(self.__pending_data_requests) > 0):
            self.__pending_data_requests[0].setStatus(RequestStatus.BEING_FULFILLED)
            self.__data_connection = self.establishDataStream(self.__pending_data_requests[0])
        # Got request to work with
        if not self.__data_connection is None:
            if self.__data_connection.transferBatch():
                self.__pending_data_requests.pop(0).setStatus(RequestStatus.DONE)
                self.__data_connection = None

# TODO: Rewrite using memory manager
    def establishDataStream(self, request : DataRequest) -> DataTransferStream:
        # PULL case
        if request.getType() == DataStreamType.PULL:
            temp = DataTransferStream(
                origin=self._global_mem,
                work_indexes_origin=request.getDirtyIndexes(),
                destination=self._local_mem,
                work_indexes_destination=self._local_mem.
            )
        # PUSH case
        else:
            temp = DataTransferStream(
                origin=self._local_mem,
                work_indexes_origin=request.getDirtyIndexes(),
                destination=self._global_mem,
                work_indexes_destination=
            )