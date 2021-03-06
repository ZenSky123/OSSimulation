from algorithm.RoundRobin import Scheduler


def testRoundRobin(filename='default.dat'):
    filepath = 'data/{}'.format(filename)

    scheduler = Scheduler()
    scheduler.load(filepath)
    scheduler.run_until_complete()
    scheduler.analysis("RoundRobin")
