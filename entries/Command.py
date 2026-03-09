from supports.UnitType import UnitType

class Command:
    def __init__(self, command_reciever_type : UnitType, addr_start : int, addr_end : int):
        if addr_end < 0 or addr_start < 0:
            raise IndexError("E: Command is being created with negative address index")
        self.__type__ = command_reciever_type
        self.__start_index__ = addr_start
        self.__end_index__ = addr_end


    def getWorkAddresses(self):
        return self.__start_index__, self.__end_index__

    def getCommandType(self):
        return self.__type__

    def __str__(self):
        return f"{self.__type__.name}_command({self.__start_index__}, {self.__end_index__})"