import msgs.Command
from actions.ActionInterface import ActionInterface


class PostNewCommand(ActionInterface):
    def __init__(self, new_command : msgs.Command.Command):
        self.command = new_command

    def enact(self, sim):
        print(str(self.command))  # For Debug