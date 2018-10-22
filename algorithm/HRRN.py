from model.BaseSchduler import BaseSchduler


class Scheduler(BaseSchduler):
    def __init__(self):
        super().__init__()

    def dispatch(self):
        if self.process_candidate:
            self.update(1)
            return self.process_candidate.pop(0)
        else:
            return None

    def reorder(self):
        """HRRN算法需要将R值最高的进程排在最前面 R= 等待时间/执行时间"""
        self.process_candidate.sort(key=lambda p: self.process_wait_time[p] / (p.cputime + 1))
