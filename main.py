from util.ran_data import generate_random_data
from test.testFCFS import testFCFS
from test.testRoundRobin import testRoundRobin
from test.testSJF import testSJF
from test.testSRTF import testSRTF
from test.testHRRN import testHRRN
from test.testMFQ import testMFQ

if __name__ == '__main__':
    generate_random_data(5, 'default.dat')
    testFCFS('default.dat')
    testRoundRobin('default.dat')
    testSJF('default.dat')
    testSRTF('default.dat')
    testHRRN('default.dat')
    testMFQ('default.dat')
