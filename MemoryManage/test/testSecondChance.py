from model import CPU
from algorithm.SecondChance import MMU
from . import MEMORY_SIZE


def testSecondChance():
    cpu = CPU(MMU(MEMORY_SIZE))
    cpu.run_until_complete()
    cpu.analysis('SecondChance')
