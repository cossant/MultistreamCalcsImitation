from Simulator import Simulator
from actions.StartTask import StartTask
from agents.AgentInterface import AgentInterface
from entries.Command import Command
from agents.TPC_Device import TPC_Device
from entries.Transaction import Transaction
from managers.MemorySpace import MemorySpace
from supports.CompletionStatus import CompletionStatus
from supports.GLOBAL_CONSTANTS import COMPUTING_UNITS_COUNT

# Has privileged access to global memory through sim.getMemory()
class CommandDistributionManager(AgentInterface):
    def __init__(self):
        self.__pending_transactions = []
        self.__wip_transactions = []
        self.__transaction_aliases = set()

    def tick(self, sim : Simulator):
        finished_transactions = self.__clearCompletedTransactions()
        self.__freeTransactionMemory(sim, finished_transactions)
        free_devices_aliases = sim.getFreeDevicesAliases()
        free_devices_aliases = self.__expandActiveTransactions(sim, free_devices_aliases)
        self.__activatePendingTransactions(sim, free_devices_aliases)

        # TODO: Continue here...

    def putCommand(self, command : Command):
        # Reformatting command as transaction
        issued_transaction_id = self.issueUnusedAlias()
        self.__transaction_aliases.add(issued_transaction_id)
        self.__pending_transactions.append(Transaction(command, issued_transaction_id))

    def issueUnusedAlias(self):
        proposed_id = 0
        while f"transaction_{str(proposed_id)}" in self.__transaction_aliases:
            proposed_id += 1
        return f"transaction_{str(proposed_id)}"


    def __clearCompletedTransactions(self):
        erased_transactions = [transaction for transaction in self.__wip_transactions if transaction.isComplete]
        for transaction in erased_transactions:
            self.__wip_transactions.remove(transaction)
            self.__transaction_aliases.remove(transaction.getName())
        return erased_transactions


    def __freeTransactionMemory(self, sim : Simulator, transactions : list[Transaction]):
        for transaction in transactions:
            sim.getMemory().free_memory(transaction.getName(), [transaction.getGlobalMemorySpan()])


    def __expandActiveTransactions(self,sim, available_devices : list[str]):
        if len(available_devices) == 0:
            return available_devices
        global_mem = sim.getMemory()
        for transaction in self.__wip_transactions:
            for task_id in range(transaction.getTaskCount()):
                if transaction.isTaskStatus(task_id, CompletionStatus.PENDING):
                    task = transaction.getTask(task_id)
                    task_address_span = task.getWorkAddresses()
                    if not global_mem.isLocked(task_address_span):
                        global_mem.lock_memory([task_address_span], transaction.getName())
                        transaction.setTaskAssigned(task_id)
                        sim.scheduleAction(StartTask(task, available_devices.pop()))
                        if len(available_devices) == 0:
                            return available_devices
        return available_devices


    def __activatePendingTransactions(self, sim,  available_devices : list[str]):
        if len(available_devices) == 0:
            return available_devices
        global_mem = sim.getMemory()
        activated_transactions = []
        for transaction in self.__pending_transactions:
            activated = False
            for task_id in range(transaction.getTaskCount()):
                task = transaction.getTask(task_id)
                task_address_span = task.getWorkAddresses()
                if not global_mem.isLocked(task_address_span):
                    global_mem.lock_memory([task_address_span], transaction.getName())
                    transaction.setTaskAssigned(task_id)
                    sim.scheduleAction(StartTask(task, available_devices.pop()))
                    activated = True
                    if len(available_devices) == 0:
                        break
            if activated:
                activated_transactions.append(transaction)
            if len(available_devices) == 0:
                break
        for transaction in activated_transactions:
            self.__pending_transactions.remove(transaction)
            self.__wip_transactions.append(transaction)
        return available_devices
 #TODO: Refactor with round-robin in second (inside active transactions) phase + use ChatGPT recommendations



