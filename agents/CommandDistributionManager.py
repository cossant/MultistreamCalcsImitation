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
        finished_transactions = self.__clearCompletedTransactions(sim)
        self.__freeTransactionMemory(sim, finished_transactions)
        free_devices_aliases = sim.getFreeDevicesAliases()
        free_devices_aliases = self.__expandActiveTransactions(sim, free_devices_aliases)
        self.__activatePendingTransactions(sim, free_devices_aliases)

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

    def closeTask(self, transaction_name : str, task_internal_index : int):
        mother_transaction = next((transaction for transaction in self.__wip_transactions if transaction.getName() == transaction_name),None)
        if mother_transaction is None:
            raise RuntimeError("Attempting to close non-existing transaction")
        mother_transaction.setTaskComplete(task_index=task_internal_index)


    def __clearCompletedTransactions(self, sim : Simulator):
        erased_transactions = [transaction for transaction in self.__wip_transactions if transaction.isComplete]
        for transaction in erased_transactions:
            sim.getMemory().free_memory(transaction.getName(), [transaction.getGlobalMemorySpan()])
            self.__wip_transactions.remove(transaction)
            self.__transaction_aliases.remove(transaction.getName())
        return erased_transactions


    def __freeTransactionMemory(self, sim : Simulator, transactions : list[Transaction]):
        for transaction in transactions:
            sim.getMemory().free_memory(transaction.getName(), [transaction.getGlobalMemorySpan()])


    # "Round robin" tasks distribution between already started transactions
    def __expandActiveTransactions(self,sim, available_devices : list[str]):
        global_mem = sim.getMemory()
        # Transactions which still have Pending tasks in them
        partially_activated_transactions = [transaction for transaction in self.__wip_transactions
                                            if any([transaction.isTaskStatus(task_id, CompletionStatus.PENDING)
                                                    for task_id in range(transaction.getTaskCount())])]
        prioritized_transaction_id = 0
        while available_devices and partially_activated_transactions:
            current_transaction = partially_activated_transactions[prioritized_transaction_id]
            task = current_transaction.getRunnableTaskId(global_mem)
            if task is not None:
                available_devices = self.__assign_task(sim, global_mem, current_transaction, task, available_devices)
            else:
                partially_activated_transactions.remove(current_transaction)
                prioritized_transaction_id -= 1
            prioritized_transaction_id += 1
            prioritized_transaction_id %= partially_activated_transactions
            if not available_devices:
                break
        return available_devices


    def __activatePendingTransactions(self, sim,  available_devices : list[str]):
        global_mem = sim.getMemory()
        activated_transactions = []
        for transaction in self.__pending_transactions:
            activated = False # Flag if this transaction should be moved from "pending" to "active"
            task = transaction.getRunnableTaskId(global_mem)
            while task is not None and available_devices:
                apply_lock = not transaction in activated_transactions
                available_devices = self.__assign_task(sim, global_mem, transaction, task, available_devices, transaction_activation = apply_lock)
                task = transaction.getRunnableTaskid(global_mem)
                activated = True # Mark this transaction to be moved to "activated"
            if activated:
                activated_transactions.append(transaction)
            if not available_devices:
                break
        for transaction in activated_transactions:
            self.__pending_transactions.remove(transaction)
            self.__wip_transactions.append(transaction)
        return available_devices

    def __assign_task(self,sim : Simulator, memory : MemorySpace, transaction : Transaction, task : Command, devices_name_list : list[str], transaction_activation = False):
        if transaction_activation:
            memory.lock_memory([transaction.getGlobalMemorySpan()], transaction.getName())
        task_index = transaction.getTasks().index(task)
        transaction.setTaskAssigned(task_index)
        sim.scheduleAction(StartTask(task, task_index, devices_name_list.pop(), transaction.getName()))
        return devices_name_list





