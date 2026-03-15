from resources.DataTransferStream import DataTransferStream
from managers.MemorySpace import MemorySpace
from assets.DataStreamCondition import DataStreamCondition
from assets.GLOBAL_CONSTANTS import WORK_MAX_BATCH_SIZE
from assets.UnitType import UnitType


# Holds information and data stream of current calculation task, which is being implemented by the means of a holding TPC device
class TaskSession:
    def __init__(self,
                 task_source: str,
                 task_index : int,
                 resource_type : UnitType,
                 global_memspace : MemorySpace, global_mem_diapasons : list[tuple[int, int]],
                 local_memspace : MemorySpace, local_mem_diapasons : list[tuple[int, int]]):
        self.__global_memspace = global_memspace
        self.__global_mem_diapasons = global_mem_diapasons
        self.__local_memspace = local_memspace
        self.__local_mem_diapasons = local_mem_diapasons
        self.__data_stream = DataTransferStream(origin=global_memspace, work_indexes_origin=global_mem_diapasons,
                                                destination=local_memspace, work_indexes_destination=local_mem_diapasons)
        self.__size = self.__data_stream.getTotalElementsCount()
        self.__processed_data_count = 0
        self.__status = DataStreamCondition.PULLING
        self.__task_owner = task_source
        self.__task_type = resource_type
        self.__unit_workbatch_size = WORK_MAX_BATCH_SIZE[self.__task_type]
        self.__task_index = task_index

    def getOwner(self):
        return self.__task_owner

    def getTaskIndex(self):
        return self.__task_index

    def getProgress(self):
        return f"{self.__processed_data_count}/{self.__data_stream.getTotalElementsCount()}"

    def getLocalDiapasons(self):
        return self.__local_mem_diapasons


    # TODO: Better to rewrite with explicit state machine
    def tick(self,sim, tpc_device):
        # Data transferring
        transfer_finished = False
        if self.__status in [DataStreamCondition.PULLING, DataStreamCondition.PUSHING]:
            transfer_finished = self.__data_stream.transferBatch()
        # Checking if enough data transferred to start a new calculations
        awaiting_data_count = self.__data_stream.getMovedElementsCount() - self.__processed_data_count
        if (awaiting_data_count >= self.__unit_workbatch_size or self.__data_stream.isCompleted()) and tpc_device.isUnitFree(self.__task_type):
            prepared_data_indexes = self.__data_stream.getDestinationIndexes()[self.__processed_data_count : self.__data_stream.getMovedElementsCount()]
            prepared_data_indexes = prepared_data_indexes[:self.__unit_workbatch_size]
            tpc_device.runCalculations(prepared_data_indexes, self.__task_type)

            self.__processed_data_count += len(prepared_data_indexes)

        if transfer_finished and self.__status == DataStreamCondition.PULLING:
            self.__status = DataStreamCondition.AWAITING

        # Creating new pushing stream if all data is calculated
        if self.__processed_data_count == self.__size and self.__status != DataStreamCondition.PUSHING:
            self.__data_stream = DataTransferStream(
                origin=self.__local_memspace,
                work_indexes_origin=self.__local_mem_diapasons,
                destination=self.__global_memspace,
                work_indexes_destination=self.__global_mem_diapasons
            )
            self.__status = DataStreamCondition.PUSHING

        if transfer_finished and self.__status == DataStreamCondition.PUSHING:
            tpc_device.submit_current_task(sim, self.__task_owner)




