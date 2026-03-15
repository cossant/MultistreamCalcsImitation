from __future__ import annotations
from agents import CommandGenerator
from Simulator import Simulator
from agents.TPC_Device import TPC_Device
from assets.GLOBAL_CONSTANTS import TOTAL_HBM_MEMORY

environment = Simulator(commands_source=CommandGenerator.CommandGenerator(TOTAL_HBM_MEMORY, 4, 1), tick_duration_seconds=0.5)
environment.registerAgent("tpc_1", TPC_Device())
environment.registerAgent("tpc_2", TPC_Device())
environment.registerAgent("tpc_3", TPC_Device())
environment.registerAgent("tpc_4", TPC_Device())
environment.registerAgent("tpc_5", TPC_Device())
environment.registerAgent("tpc_6", TPC_Device())
environment.registerAgent("tpc_7", TPC_Device())
environment.registerAgent("tpc_8", TPC_Device())


environment.runSimulation()
