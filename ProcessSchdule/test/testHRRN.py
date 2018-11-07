from algorithm.HRRN import Scheduler


def testHRRN(filename='default.dat'):
    filepath = 'data/{}'.format(filename)

    scheduler = Scheduler()
    scheduler.load(filepath)
    scheduler.run_until_complete()
    scheduler.analysis("HRRN")
