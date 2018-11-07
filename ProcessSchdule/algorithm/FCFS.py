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
        """FCFS算法不需要对进程队列重新排序"""
