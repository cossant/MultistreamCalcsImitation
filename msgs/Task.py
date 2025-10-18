from msgs.Command import Command
from singletons.UnitType import UnitType


class Task(Command):
    def __init__(self, command_reciever_type: UnitType, addr_start: int, addr_end: int, data_lock_indexes):
        super().__init__(command_reciever_type, addr_start, addr_end)
        self.__lock_start, self.__lock_end = data_lock_indexes