from msgs.Command import Command
from supports.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY_IN_BYTES

class Transaction:
    def __init__(self, raw_command : Command):
        self.__total_transaction_size = self._calculateCommandSize(raw_command)
        self.__global_mem_start, self.__global_mem_end = raw_command.getWorkAddresses()
        self.__tasks = self._decomposeCommand(raw_command)
        self.__task_count = len(self.__tasks)
        self.__tasks_completion_status = [False for _ in range(self.__task_count)]
        self.__tasks_assignment_status = [False for _ in range(self.__task_count)]
        self.__transaction_active = False
        self.__commands_type = raw_command.getCommandType()

    def _decomposeCommand(self, huge_command: Command):
        command_type = huge_command.getCommandType()
        processed_objects = 0
        artificial_tasks = []
        while processed_objects < self.__total_transaction_size:
            left_unprocessed = self.__total_transaction_size - processed_objects
            batch_size = TOTAL_TPC_MEMORY_IN_BYTES if left_unprocessed > TOTAL_TPC_MEMORY_IN_BYTES else left_unprocessed
            artificial_tasks.append(
                Command(
                    command_type,
                    self.__global_mem_start + processed_objects,
                    self.__global_mem_start + processed_objects + batch_size,
                )
            )
            processed_objects = processed_objects + batch_size
        return artificial_tasks

    def _calculateCommandSize(self, command: Command):
        start_index, end_index = command.getWorkAddresses()
        return end_index - start_index

    def isTransactionActive(self):
        for assigned in self.__tasks_assignment_status:
            if assigned:
                return True
        return False

    def isTransactionComplete(self):
        for status_complete in self.__tasks_completion_status:
            if not status_complete:
                return False
        return True

    def isTaskComplete(self, task_index):
        return self.__tasks_completion_status[task_index]

    def isTaskAssigned(self, task_index):
        return self.__tasks_assignment_status[task_index]

    def getTaskCount(self):
        return self.__task_count

    def getTask(self, task_index):
        return self.__tasks[task_index]

    def getTasks(self):
        return self.__tasks

    def getTaskInfo(self, task_id):
        return self._calculateCommandSize(self.__tasks[task_id]), self.__commands_type

    def setTaskComplete(self, task_index):
        if self.__tasks_completion_status[task_index] == True:
            raise ValueError("Trying to mark completion of a task already marked as completed")
        self.__tasks_completion_status[task_index] = True

    def setTaskAssigned(self, task_index):
        if self.__tasks_assignment_status[task_index] == True:
            raise ValueError("Trying to mark assignation of a task already marked as assigned")
        self.__tasks_assignment_status[task_index] = True