from algorithm.SJF import Scheduler


def testSJF(filename='default.dat'):
    filepath = 'data/{}'.format(filename)

    scheduler = Scheduler()
    scheduler.load(filepath)
    scheduler.run_until_complete()
    scheduler.analysis("SJF")
