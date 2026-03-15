import random
from actions.StartTask import StartTask
from interfaces.AgentInterface import AgentInterface
from entries.Command import Command
from entries.Transaction import Transaction
from managers.MemorySpace import MemorySpace
from assets.CompletionStatus import CompletionStatus


# Has privileged access to global memory through sim.getMemory()
# TODO: Better rewrite, unifying "expand" and "activate" functions into one
class CommandDistributionManager(AgentInterface):
    def __init__(self):
        self.__pending_transactions = []
        self.__active_transactions = []
        self.__transaction_aliases = set()

    def tick(self, sim):
        self.__clearCompletedTransactions(sim)
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
        mother_transaction = next((transaction for transaction in self.__active_transactions if transaction.getName() == transaction_name), None)
        if mother_transaction is None:
            raise RuntimeError("Attempting to close non-existing transaction")
        mother_transaction.setTaskComplete(task_index=task_internal_index)


    def __clearCompletedTransactions(self, sim):
        completed_transactions = [transaction for transaction in self.__active_transactions if transaction.isComplete()]
        for transaction in completed_transactions:
            print(f"-------------Deleting completed user Command {transaction.getGlobalMemorySpan()} {transaction.getTasks()[0].getCommandType()}")
            sim.getMemory().free_memory(transaction.getName(), [transaction.getGlobalMemorySpan()])
            self.__active_transactions.remove(transaction)
            self.__transaction_aliases.remove(transaction.getName())
        return completed_transactions



    # "Round robin" tasks distribution between already started transactions
    def __expandActiveTransactions(self,sim, available_devices : list[str]):
        global_mem = sim.getMemory()
        # Transactions which still have Pending tasks in them
        partially_activated_transactions = [transaction for transaction in self.__active_transactions
                                            if any([transaction.isTaskStatus(task_id, [CompletionStatus.PENDING])
                                                    for task_id in range(transaction.getTaskCount())])]
        prioritized_transaction_id = 0
        while available_devices and partially_activated_transactions:
            prioritized_transaction_id %= len(partially_activated_transactions)
            current_transaction = partially_activated_transactions[prioritized_transaction_id]
            task = current_transaction.getRunnableTaskId(global_mem)
            if task is not None:
                available_devices = self.__assign_task(sim, global_mem, current_transaction, task, available_devices)
            else:
                partially_activated_transactions.remove(current_transaction)
                prioritized_transaction_id -= 1
            prioritized_transaction_id += 1
            if not available_devices:
                break
        return available_devices


    def __activatePendingTransactions(self, sim,  available_devices : list[str]):
        global_mem = sim.getMemory()
        for transaction in self.__pending_transactions:
            task = transaction.getRunnableTaskId(global_mem)
            while task is not None and available_devices:
                available_devices = self.__assign_task(sim, global_mem, transaction, task, available_devices)
                task = transaction.getRunnableTaskId(global_mem)
            if not available_devices:
                break
        return available_devices

    def __assign_task(self, sim, memory : MemorySpace, transaction : Transaction, task : Command, devices_name_list : list[str]):
        if not transaction.isActive():
            self.__activate_transaction(memory, transaction)
        task_index = transaction.getTasks().index(task)
        transaction.setTaskAssigned(task_index)
        sim.scheduleAction(StartTask(task,task_index,devices_name_list.pop(random.randrange(len(devices_name_list))),transaction.getName()))
        return devices_name_list

    def __activate_transaction(self, global_memory : MemorySpace, transaction : Transaction):
        global_memory.lock_memory([transaction.getGlobalMemorySpan()], transaction.getName())
        self.__pending_transactions.remove(transaction)
        self.__active_transactions.append(transaction)

