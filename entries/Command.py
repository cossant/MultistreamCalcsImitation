from assets.UnitType import UnitType
import deal

class Command:
    @deal.pre(lambda self, command_receiver_type, addr_start, addr_end: 
              addr_start >= 0 and addr_end >= 0, message="E: Command is being created with negative address index")
    @deal.pre(lambda self, command_receiver_type, addr_start, addr_end: 
              addr_start <= addr_end, message="E: End index is less than Start")
    def __init__(self, command_receiver_type : UnitType, addr_start : int, addr_end : int):
        self.__type__ = command_receiver_type
        self.__start_index__ = addr_start
        self.__end_index__ = addr_end

    def __len__(self):
        return self.__end_index__ + 1 - self.__start_index__

    def __str__(self):
        return f"{self.__type__.name}_command({self.__start_index__}, {self.__end_index__})"

    def getWorkAddresses(self):
        return self.__start_index__, self.__end_index__

    def getCommandType(self):
        return self.__type__