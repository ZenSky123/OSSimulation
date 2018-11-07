from algorithm.SRTF import Scheduler


def testSRTF(filename='default.dat'):
    filepath = 'data/{}'.format(filename)

    scheduler = Scheduler()
    scheduler.load(filepath)
    scheduler.run_until_complete()
    scheduler.analysis("SRTF")
