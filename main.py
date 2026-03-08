from __future__ import annotations
from agents import CommandGenerator
from Simulator import Simulator


environment = Simulator(commands_source=CommandGenerator.CommandGenerator(100, 4, 1))


environment.runSimulation()