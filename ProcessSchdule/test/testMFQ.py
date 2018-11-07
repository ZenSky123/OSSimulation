from algorithm.MFQ import Scheduler


def testMFQ(filename='default.dat'):
    filepath = 'data/{}'.format(filename)

    scheduler = Scheduler()
    scheduler.load(filepath)
    scheduler.run_until_complete()
    scheduler.analysis("MFQ")
