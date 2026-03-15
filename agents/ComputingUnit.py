from interfaces.AgentInterface import AgentInterface
from managers.MemorySpace import MemorySpace
from assets.UnitType import UnitType
from assets import GLOBAL_CONSTANTS
from random import randint


class ComputingUnit(AgentInterface):
    def __init__(self, this_unit_type : UnitType, local_mem : MemorySpace):
        self.__type = this_unit_type
        self.__local_memory = local_mem
        self.__work_duration_fork = GLOBAL_CONSTANTS.WORK_DURATION_IN_TICKS_FORK[this_unit_type]
        self.__work_batch = GLOBAL_CONSTANTS.WORK_MAX_BATCH_SIZE[this_unit_type]
        self.__work_duration_left = None
        self.__assigned_indexes : list[int] | None= None

    def tick(self, sim):
        if self.__assigned_indexes is not None:
            #print(f"{self.__type} unit is working with {self.__work_duration_left} ticks left")
            if self.__work_duration_left == 0:
                self.touchIndexes(self.__assigned_indexes)
                self.__work_duration_left = None
                self.__assigned_indexes = None
            else:
                self.__work_duration_left -= 1

    def touchIndexes(self, indexes : list[int]):
        for index in indexes:
            self.__local_memory.imitateRead(index)
            self.__local_memory.imitateWrite(index, 1)

    def assignCalculations(self, task_indexes):
        if self.__assigned_indexes is not None:
            raise RuntimeError("Attempting to run task on busy computing unit")
        else:
            self.__assigned_indexes = task_indexes
            self.__work_duration_left = self._estimateWorktime()

    def getUnitType(self):
        return self.__type

    def isFree(self):
        return True if self.__assigned_indexes is None else False

    def _estimateWorktime(self):
        return randint(*self.__work_duration_fork)