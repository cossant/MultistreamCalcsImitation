from agents.AgentInterface import AgentInterface
from entries.Command import Command
from agents.TPC_Device import TPC_Device
from entries.Transaction import Transaction
from supports.GLOBAL_CONSTANTS import COMPUTING_UNITS_COUNT

class CommandDistributionManager(AgentInterface):
    def __init__(self):
        self.__transaction_stack = []
        self.__wip_transactions = []
        self.__transaction_alias_ids = set()

    def tick(self, sim):
        # TODO: Continue here...
        # 1. Close completed threads
        # 2. Free resources
        # 3. Open pending threads

    def putCommand(self, command : Command):
        # Reformatting command as transaction
        issued_transaction_id = self.issueUnusedId()
        self.__transaction_alias_ids.add(issued_transaction_id)
        self.__transaction_stack.append(Transaction(command, issued_transaction_id))

    def issueUnusedId(self):
        proposed_index = 0
        while proposed_index in self.__transaction_alias_ids:
            proposed_index += 1
        return proposed_index



