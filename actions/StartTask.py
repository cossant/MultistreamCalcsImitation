from actions.ActionInterface import ActionInterface
from agents.TPC_Device import TPC_Device
from entries.Command import Command


class StartTask(ActionInterface):
    def __init__(self, task : Command, worker_alias : str):
        self.__task = task
        self.__worker_name = worker_alias

    def enact(self, sim ):