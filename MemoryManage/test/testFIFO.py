from model import CPU
from algorithm.FIFO import MMU
from . import MEMORY_SIZE


def testFIFO():
    cpu = CPU(MMU(MEMORY_SIZE))
    cpu.run_until_complete()
    cpu.analysis('FIFO')
