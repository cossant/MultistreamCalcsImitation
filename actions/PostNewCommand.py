import entries.Command
from interfaces.ActionInterface import ActionInterface


class PostNewCommand(ActionInterface):
    def __init__(self, new_command : entries.Command.Command):
        self.command = new_command

    def enact(self, sim):
        print(f"NEW USER COMMAND: {str(self.command)}")
        sim.getManager().putCommand(self.command)