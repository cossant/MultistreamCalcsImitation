from Simulator import Simulator
from actions.ActionInterface import ActionInterface
from agents.TPC_Device import TPC_Device
from entries.Command import Command


class StartTask(ActionInterface):
    def __init__(self, task : Command, worker_alias : str, thread_alias : str):
        self.__task = task
        self.__worker_name = worker_alias
        self.__requester_name = thread_alias

    def enact(self, sim : Simulator):
        worker = sim.getWorker(self.__worker_name)
        if not isinstance(worker, TPC_Device):
            raise RuntimeError("Not TPC device is chosen as worker")
        if not worker.isFree():
            raise RuntimeError("Worker who's already busy is chosen for rask assignation")
        worker.assignTask(self.__task, sim.getMemory(), self.__requester_name)
