from util import ran_data
from test.testFIFO import testFIFO
from test.testSecondChance import testSecondChance
from test.testLFU import testLFU

if __name__ == '__main__':
    ran_data()
    testFIFO()
    testSecondChance()
    testLFU()