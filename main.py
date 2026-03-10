from __future__ import annotations
from agents import CommandGenerator
from Simulator import Simulator
from supports.GLOBAL_CONSTANTS import TOTAL_HBM_MEMORY

environment = Simulator(commands_source=CommandGenerator.CommandGenerator(TOTAL_HBM_MEMORY, 4, 1))


environment.runSimulation()