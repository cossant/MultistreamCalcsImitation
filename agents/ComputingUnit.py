from agents.AgentInterface import AgentInterface
from supports.UnitType import UnitType
from supports import GLOBAL_CONSTANTS
from msgs.Command import Command
from random import randint
from ControlUnit import ControlUnit
from msgs.DataRequest import DataRequest
from agents.DataTransferStream import DataTransferStream
from supports.DataStreamType import DataStreamType


class ComputingUnit(AgentInterface):
    def __init__(self, this_unit_type : UnitType, CU : ControlUnit):
        self.__type__ = this_unit_type
        self.__work_duration_fork__ = GLOBAL_CONSTANTS.WORK_DURATION_IN_TICKS_FORK[this_unit_type]
        self.__work_batch__ = GLOBAL_CONSTANTS.WORK_MAX_BATCH_SIZE_IN_BYTES[this_unit_type]
        self.__controller = CU
        self.__work_duration_left = 0
        self.__task = None
        self.__processing= False
        self.__data_request = None
        self.__assigned_local_memory_range = []
        self.__processed_data_local_index = 0

    def assignTask(self, command : Command):
        if not command.getCommandType() == self.__type__:
            raise TypeError("E: Computing Unit somehow received command of a wrong type")
        self.__task = command
        requested_data_size = command.getWorkAddresses()[1] - command.getWorkAddresses()[0]
        self.__data_request = DataRequest(
            DataStreamType.PULL,
            requested_data_size,
            [command.getWorkAddresses()])
        self.__controller.registerDataRequest(self.__data_request)

    def getUnitType(self):
        return self.__type__

    def isFree(self):
        return True if self.__task is None else False

    def _estimateWorktime(self):
        return randint(*self.__work_duration_fork__)

    def _requestDataPull(self):
        raise NotImplementedError()

    def _requestDataPush(self):
        raise NotImplementedError()

    def _workOnDataBatch(self):
        raise NotImplementedError()

    def tick(self, sim):
        if self.__task is None:
            return
        # TODO: Data pull check

    # def _checkDataPullPossibility(self):
    #     # Checking if any more data could be pulled
    #     global_mem_start, global_mem_end = self.__task.getWorkAddresses()
    #     total_task_data_length = global_mem_end - global_mem_start
    #     local_copy_length = len(self.__local_memory)
    #     if local_copy_length < total_task_data_length:
    #         # Calculating next data pull required size
    #         no_copied_data_size = total_task_data_length - local_copy_length
    #         requested_data_size = GLOBAL_CONSTANTS.DATA_TRANSACTION_MAX_SIZE_IN_BYTES \
    #             if no_copied_data_size > GLOBAL_CONSTANTS.DATA_TRANSACTION_MAX_SIZE_IN_BYTES \
    #             else no_copied_data_size
    #         self._requestDataPull(requested_data_size)
