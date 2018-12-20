from model import CPU
from algorithm.LRU import MMU
from . import MEMORY_SIZE


def testLRU():
    cpu = CPU(MMU(MEMORY_SIZE))
    cpu.run_until_complete()
    cpu.analysis('LRU')
