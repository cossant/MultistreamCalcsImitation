from interfaces.ActionInterface import ActionInterface


class CloseTask(ActionInterface):
    def __init__(self, transaction_alias : str, task_index : int):
        self.__task_index = task_index
        self.__transaction_alias = transaction_alias

    def enact(self, sim):
        print(f"-----------------------------------------------------task num{self.__task_index} fulfilled for {self.__transaction_alias}")
        sim.getManager().closeTask(self.__transaction_alias, self.__task_index)