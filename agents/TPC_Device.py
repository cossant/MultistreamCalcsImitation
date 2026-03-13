from agents.AgentInterface import AgentInterface
from agents.ComputingUnit import ComputingUnit
from agents.DataTransferStream import DataTransferStream
from entries.Command import Command
from entries.TaskSession import TaskSession
from managers.MemorySpace import MemorySpace
from supports.DataStreamCondition import DataStreamCondition
from supports.UnitType import UnitType
from supports.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY

# Encapsulating 3 processing units
# and implements logic for Controlling Unit without encapsulating it into separate class
# Has NO task queue - all task queuing happens in CommandDistributionManager and Transactions
class TPC_Device(AgentInterface):
    def __init__(self):
        self.__memory = MemorySpace(TOTAL_TPC_MEMORY)
        self.__task_session : TaskSession | None = None
        self.__VPU = ComputingUnit(UnitType.VPU, self.__memory)
        self.__ME = ComputingUnit(UnitType.ME, self.__memory)
        self.__FE = ComputingUnit(UnitType.FE, self.__memory)

    def isFree(self):
        return self.__task_session is None

    def isUnitFree(self, unit_type : UnitType):
        if unit_type == UnitType.FE:
            return self.__FE.isFree()
        elif unit_type == UnitType.ME:
            return self.__ME.isFree()
        elif unit_type == UnitType.VPU:
            return self.__VPU.isFree()

    def runCalculations(self, local_mem_indexes : list[int], unit_type : UnitType):
        if unit_type == UnitType.FE:
            self.__FE.assignCalculations(local_mem_indexes)
        elif unit_type == UnitType.ME:
            self.__ME.assignCalculations(local_mem_indexes)
        elif unit_type == UnitType.VPU:
            self.__VPU.assignCalculations(local_mem_indexes)
        else:
            raise RuntimeError("Unknown calculation unit type used in running calculations")


    def assignTask(self, task : Command, global_memory_space : MemorySpace, blocker_name : str):
        self.__task_session = TaskSession(task_source=blocker_name,
                                          resource_type=task.getCommandType(),
                                          global_memspace=global_memory_space, global_mem_diapasons=task.getWorkAddresses(),
                                          local_memspace=self.__memory, local_mem_diapasons=self.__memory.request_memory(len(task), blocker_name))

    def tick(self, sim):
        if self.__task_session:
            self.__task_session.tick(self)
        self.__FE.tick(sim)
        self.__ME.tick(sim)
        self.__VPU.tick(sim)

    def close_task(self, task_lock_name : str):
        #TODO: Launch action freeing global and local mem