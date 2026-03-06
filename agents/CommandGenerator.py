from numpy.random import normal as normal_random
from numpy.random import randint

from actions.PostNewCommand import PostNewCommand
from agents.AgentInterface import AgentInterface
from supports.UnitType import UnitType
from warnings import warn
from msgs.Command import Command

class CommandGenerator(AgentInterface):
    def __init__(self, max_valid_memory_address: int, m_exp_tacts: int, deviation: int):
        self.__m_expect_tacts = m_exp_tacts
        self.__standard_deviation = deviation
        self.__total_memory_size = max_valid_memory_address
        if (m_exp_tacts - 3 * deviation) <= 0:
            warn("Command generator set up to touch 0 latency with its 3dev radius")
        self.__ticks_to_new_command = self.__getNewCommandWaitPeriod()

    def tick(self, sim):
        new_command = self.__checkForCommand()
        if not new_command is None:
            sim.scheduleAction(PostNewCommand(new_command))

    # Returns msgs.Command if such was received this tick
    def __checkForCommand(self):
        if self.__ticks_to_new_command == 0:
            self.__ticks_to_new_command = self.__getNewCommandWaitPeriod()
            return self.__generateCommand()
        else:
            self.__ticks_to_new_command -= 1
            return None

    def __getNewCommandWaitPeriod(self):
        ticks = int(normal_random(self.__m_expect_tacts, self.__standard_deviation))
        return ticks if ticks >= 0 else 0

    def __generateCommand(self):
        command_type = UnitType(randint(low=0, high=(len(UnitType)-1)))
        command_addresses = sorted([randint(self.__total_memory_size), randint(self.__total_memory_size)])
        return Command(command_type, *command_addresses)
