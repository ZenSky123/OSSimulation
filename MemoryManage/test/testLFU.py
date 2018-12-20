from model import CPU
from algorithm.LFU import MMU
from . import MEMORY_SIZE


def testLFU():
    cpu = CPU(MMU(MEMORY_SIZE))
    cpu.run_until_complete()
    cpu.analysis('LFU')
