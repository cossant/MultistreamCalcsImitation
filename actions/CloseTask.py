from actions.ActionInterface import ActionInterface
from Simulator import Simulator
from entries.Command import Command


class CloseTask(ActionInterface):
    def __init__(self, transaction_alias : str, task_index : int):
        self.__task_index = task_index
        self.__transaction_alias = transaction_alias

    def enact(self, sim : Simulator):
        sim.getManager().closeTask(self.__transaction_alias, self.__task_index)