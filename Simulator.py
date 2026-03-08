from time import sleep

from agents.AgentInterface import AgentInterface
from actions.ActionInterface import ActionInterface


class Simulator:
    def __init__(self, commands_source : AgentInterface, tick_duration_seconds : int = 1):
        self.__tickable_agents = {"commands_sequence" : commands_source}
        self.__pending_actions = []
        self.__tick_duration = tick_duration_seconds

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