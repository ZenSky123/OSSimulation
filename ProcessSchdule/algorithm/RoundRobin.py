from model.BaseSchduler import BaseSchduler


class Scheduler(BaseSchduler):
    def __init__(self):
        super().__init__()

    def dispatch(self):
        if self.process_candidate:
            self.set_chip(25)
            self.update(1)
            return self.process_candidate.pop(0)
        else:
            return None

    def reorder(self):
        """RoundRobin算法不需要对进程队列重新排序，只需要每次时间片归零时没执行完的进程直接放到队尾就好"""
