from time import sleep

from agents.AgentInterface import AgentInterface
from actions.ActionInterface import ActionInterface
from agents.CommandDistributionManager import CommandDistributionManager
from agents.TPC_Device import TPC_Device
from managers.MemorySpace import MemorySpace
from supports.GLOBAL_CONSTANTS import TOTAL_HBM_MEMORY


class Simulator:
    def __init__(self, commands_source : AgentInterface, tick_duration_seconds : int = 1):
        self.__global_memory = MemorySpace(TOTAL_HBM_MEMORY)
        self.__tickable_agents = {
            "command_stream" : commands_source,
            "command_manager" : CommandDistributionManager(),
        }
        self.__pending_actions = []
        self.__tick_duration = tick_duration_seconds

    # Should only be used by "Command manager" or from inside an action
    def getManager(self):
        return self.__tickable_agents["command_manager"]

    # Should only be used by "Command manager" or from inside an action
    def getMemory(self):
        return self.__global_memory

    def getFreeDevicesAliases(self):
        free_devices_names = []
        for agent_name in self.__tickable_agents.keys():
            if isinstance(self.__tickable_agents[agent_name], TPC_Device):
                free_devices_names.append(agent_name)
        return free_devices_names
                    

    def registerAgent(self, name_id : str, agent : AgentInterface):
        if name_id in self.__tickable_agents:
            raise IndexError(f"\"{name_id}\" as id already taken")
        self.__tickable_agents[name_id] = agent

    def scheduleAction(self, action : ActionInterface):
        self.__pending_actions.append(action)

    def __simulateTact(self):
        # Receiving actions from agents and scheduling them for the next tick
        for agent in self.__tickable_agents.values():
            agent.tick(self)    # agent receives Sim's self and invoke "scheduleEvent" if needed

        curr_tick_actions = self.__pending_actions
        self.__pending_actions = []

        for action in curr_tick_actions:
            action.enact(self)

    def runSimulation(self):
        while True:
            self.__simulateTact()
            sleep(self.__tick_duration)