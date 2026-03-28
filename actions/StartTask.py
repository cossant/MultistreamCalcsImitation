from interfaces.ActionInterface import ActionInterface
from agents.TPC_Device import TPC_Device
from entries.Command import Command
import deal

class StartTask(ActionInterface):
    def __init__(self, task : Command, task_inside_index : int, worker_alias : str, thread_alias : str):
        self.__task = task
        self.__task_index = task_inside_index
        self.__worker_name = worker_alias
        self.__requester_name = thread_alias

    @deal.pre(lambda self, sim: isinstance(sim.getWorker(self.__worker_name), TPC_Device),
          message="E: Not TPC device is chosen as worker", exception=RuntimeError)
    @deal.pre(lambda self, sim: sim.getWorker(self.__worker_name).isFree(),
          message="E: Worker who's already busy is chosen for rask assignation", exception=RuntimeError)
    def enact(self, sim):
        print(f"task {self.__task}:{self.__task_index} assigned on {self.__worker_name} by {self.__requester_name}")
        worker = sim.getWorker(self.__worker_name)
        worker.assignTask(self.__task, self.__task_index, sim.getMemory(), self.__requester_name)
