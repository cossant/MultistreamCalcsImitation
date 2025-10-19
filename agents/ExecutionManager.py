from msgs.Command import Command
from agents.TPC_Device import TPC_Device
from msgs.Transaction import Transaction
from singletons.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY
from singletons.GLOBAL_CONSTANTS import COMPUTING_UNITS_COUNT
from singletons.UnitType import  UnitType
from agents.MemoryManager import MemoryManager

class ExecutionManager:
    def __init__(self, memory_manager : MemoryManager):
        self.__raw_commands = []
        self.__transactions = []
        self.__slaves = [TPC_Device(memory_manager) for _ in range(COMPUTING_UNITS_COUNT)]

    def addSlave(self, new_slaves):
        for slave in new_slaves:
            self.__slaves.append(slave)

    def putCommand(self, command : Command):
        self.__raw_commands.append(command)

    def _processAcquiredCommands(self):
        while not len(self.__raw_commands) == 0:
            new_transaction = Transaction(self.__raw_commands.pop(0))
            self.__transactions.append(new_transaction)

    def _getSuitableSlave(self, required_mem_space, targeted_module_type):
        # TODO
        pass

    def tick(self):
        self._processAcquiredCommands()
        for transaction in self.__transactions:
            for task_id in range(transaction.getTaskCount()):
                if not transaction.isTaskAssigned(task_id):
                    slave = self._getSuitableSlave(*transaction.getTaskInfo(task_id))
                    if slave is not None: # TODO: Add mem accessibility check
                        #TODO: Put task in slave work
                        transaction.setTaskAssigned(task_id)


