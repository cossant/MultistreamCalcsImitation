from entries.Command import Command
from supports.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY
from supports.CompletionStatus import CompletionStatus

class Transaction:
    def __init__(self, raw_command : Command, issued_alias : str):
        self.__total_transaction_size = self._calculateCommandSize(raw_command)
        self.__global_mem_start, self.__global_mem_end = raw_command.getWorkAddresses()
        self.__command_type = raw_command.getCommandType()
        self.__tasks = self._decomposeCommand()
        self.__task_count = len(self.__tasks)
        self.__tasks_status = [CompletionStatus.PENDING for _ in range(self.__task_count)]
        self.__name = issued_alias

    def getName(self):
        return self.__name

    def getGlobalMemorySpan(self):
        return self.__global_mem_start, self.__global_mem_end

    # Cutting user command into number of artificial commands (might be just one)
    def _decomposeCommand(self):
        processed_objects = 0
        artificial_tasks : list[Command] = []
        while processed_objects < self.__total_transaction_size:
            left_unprocessed = self.__total_transaction_size - processed_objects
            batch_size = TOTAL_TPC_MEMORY if left_unprocessed > TOTAL_TPC_MEMORY else left_unprocessed
            artificial_tasks.append(
                Command(
                    self.__command_type,
                    self.__global_mem_start + processed_objects,
                    self.__global_mem_start + processed_objects + batch_size,
                )
            )
            processed_objects += batch_size
        return artificial_tasks

    def _calculateCommandSize(self, command: Command):
        start_index, end_index = command.getWorkAddresses()
        return end_index + 1 - start_index

    def isActive(self):
        for status in self.__tasks_status:
            if status is not CompletionStatus.PENDING:
                return True
        return False

    def isComplete(self):
        for status in self.__tasks_status:
            if status is not CompletionStatus.DONE:
                return False
        return True

    def isTaskStatus(self, task_index : int, acceptable_statuses : list[CompletionStatus]):
        return self.__tasks_status[task_index] in acceptable_statuses

    def getTaskCount(self):
        return self.__task_count

    def getTask(self, task_index : int):
        return self.__tasks[task_index]

    def getTasks(self):
        return self.__tasks

    def getTaskInfo(self, task_id : int):
        return self._calculateCommandSize(self.__tasks[task_id]), self.__command_type

    def setTaskComplete(self, task_index : int):
        if self.isTaskComplete(task_index):
            raise ValueError("Trying to mark completion of a task already marked as completed")
        else:
            self.__tasks_status[task_index] = CompletionStatus.DONE

    def setTaskAssigned(self, task_index : int):
        if self.isTaskAssigned(task_index):
            raise ValueError("Trying to mark assignation of a task already marked as assigned")
        self.__tasks_status[task_index] = CompletionStatus.ASSIGNED