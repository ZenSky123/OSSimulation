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
        """SJF算法需要将作业最短的排在最前面"""
        self.process_candidate.sort(key=lambda p: p.needTime)
