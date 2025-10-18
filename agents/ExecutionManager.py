from msgs.Command import Command
from msgs.Task import Task
from agents.TPC_Device import TPC_Device
from singletons.GLOBAL_CONSTANTS import TOTAL_TPC_MEMORY_IN_BYTES
from singletons.UnitType import  UnitType

class ExecutionManager:
    def __init__(self):
        self.__raw_command_buffer = []
        self.__tasks_buffer = []
        self.__slaves = []
        self.__set_up_state = True

    def assertPrepared(self):
        # TODO: Check slaves exist and counted as in global_consts
        #       Memory assigned
        #       Memory manager assigned
        self.__set_up_state = False

    def addSlave(self, new_slave : TPC_Device):
        self.__slaves.append(new_slave)

    def putCommand(self, command : Command):
        self.__raw_command_buffer.append(command)

    def tick(self):
        if self.__set_up_state:
            raise AssertionError("Execution manager is not yet asserted to be ready")
        slave_buffers_insufficient = False
        while not len(self.__raw_command_buffer) == 0:
            curr_command = self.__raw_command_buffer.pop(0)
            if self._evaluateTaskSize(curr_command) > TOTAL_TPC_MEMORY_IN_BYTES:



    def _decomposeTask(self, huge_task : Command):
        task_type = huge_task.getCommandType()
        task_size = self._evaluateTaskSize(huge_task)
        huge_start, huge_end = huge_task.getWorkAddresses()
        decomposed_objects = 0
        arriving_tasks = []
        while decomposed_objects < task_size:
            left_undecomposed = task_size - decomposed_objects
            batch_size = TOTAL_TPC_MEMORY_IN_BYTES if left_undecomposed > TOTAL_TPC_MEMORY_IN_BYTES else left_undecomposed
            arriving_tasks.append(
                Task(
                    task_type,
                    huge_start + decomposed_objects,
                    huge_start + decomposed_objects + batch_size,
                    (huge_start, huge_end)
                )
            )
            decomposed_objects = decomposed_objects + batch_size
        self._appendTasks(arriving_tasks)


    def _evaluateTaskSize(self, task : Command):
        start_index, end_index = task.getWorkAddresses()
        return end_index - start_index

    def _processTask(self):
        pass
        #TODO:

    def _appendTasks(self, arriving_tasks):
        index = 0
        for command in arriving_tasks:
            self.__command_buffer.insert(index, command)
            # TODO: Insert tasks in task queue
