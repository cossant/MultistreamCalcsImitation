import entries.Command
from Simulator import Simulator
from actions.ActionInterface import ActionInterface


class PostNewCommand(ActionInterface):
    def __init__(self, new_command : entries.Command.Command):
        self.command = new_command

    def enact(self, sim : Simulator):
        sim.getManager().putCommand(self.command)