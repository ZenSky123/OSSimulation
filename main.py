from util.ran_data import generate_random_data
from test.testFCFS import testFCFS

if __name__ == '__main__':
    generate_random_data(10, 'default.dat')
    testFCFS('default.dat')
