from time import sleep
from keyboard import is_pressed
from agents.CommandGenerator import CommandGenerator


class Ticker:
    def __init__(self, commands_source : CommandGenerator, tick_duration : int = 1):
        self.__tickable_agents = {
            "commands_stream" : commands_source
        }
        self.__tick_duration = tick_duration

    def calculateTact(self):
        agents = self.__tickable_agents
        new_command = agents["commands_stream"].checkForCommand()
        print(str(new_command) if new_command is not None else "---") # For Debug
        # TODO: Continue here

    def runSimulation(self):
        while not is_pressed('q'):
            self.calculateTact()
            sleep(self.__tick_duration)