from agents.AgentInterface import AgentInterface
from agents.ComputingUnit import ComputingUnit
from agents.DataTransferStream import DataTransferStream
from managers.MemorySpace import MemorySpace
from supports.UnitType import UnitType
from supports.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY

# Encapsulating 3 processing units
# and implements logic for Controlling Unit without encapsulating it into separate class
class TPC_Device(AgentInterface):
    def __init__(self):
        self.__memory = MemorySpace(TOTAL_TPC_MEMORY)
        self.__data_stream = None
        self.__VPU = ComputingUnit(UnitType.VPU)
        self.__ME = ComputingUnit(UnitType.ME)
        self.__FE = ComputingUnit(UnitType.FE)

    def tick(self, sim):