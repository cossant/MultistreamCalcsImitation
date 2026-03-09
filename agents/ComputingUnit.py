from agents.AgentInterface import AgentInterface
from supports.UnitType import UnitType
from supports import GLOBAL_CONSTANTS
from entries.Command import Command
from random import randint
from entries.DataRequest import DataRequest
from agents.DataTransferStream import DataTransferStream
from supports.DataStreamType import DataStreamType


class ComputingUnit(AgentInterface):
    def __init__(self, this_unit_type : UnitType):
        self.__type__ = this_unit_type
        self.__work_duration_fork__ = GLOBAL_CONSTANTS.WORK_DURATION_IN_TICKS_FORK[this_unit_type]
        self.__work_batch__ = GLOBAL_CONSTANTS.WORK_MAX_BATCH_SIZE[this_unit_type]
        self.__work_duration_left = 0
        self.__task = None

    def assignTask(self, command : Command):
        if not command.getCommandType() == self.__type__:
            raise TypeError("E: Computing Unit somehow received command of a wrong type")
        # TODO: task assignation

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
    #     blahblahlah
