from agents.ControlUnit import ControlUnit
from agents.ComputingUnit import ComputingUnit
from singletons.UnitType import UnitType
from singletons.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY
from storages.LocMem import LocMem

class TPC_Device:
    def __init__(self, memory_manager):
        self.__memory = LocMem(TOTAL_TPC_MEMORY)
        self.__CU = ControlUnit(memory_manager, self.__memory)
        self.__VPU = ComputingUnit(UnitType.VPU, self.__CU)
        self.__ME = ComputingUnit(UnitType.ME, self.__CU)
        self.__FE = ComputingUnit(UnitType.FE, self.__CU)