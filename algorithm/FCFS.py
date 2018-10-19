from queue import Queue
from model.Process import Process
from model.BaseSchduler import BaseSchduler
from collections import defaultdict


class Scheduler(BaseSchduler):
    def __init__(self):
        """
            process_unload     : 已经按照到达时间排序好的所有进程信息，还没有载入到内存中，每次载入一个则弹出一个
            process_in_memory  : 已经载入到内存的进程，这部分进程需要计算等待时间，进程执行完毕需要弹出，所以没有使用列表
            process_wait_time  : 每个进程的周转时间
            process_queue      : FCFS算法所用的队列
        """
        self.process_unloaded = []
        self.process_in_memory = set()
        self.process_wait_time = defaultdict(int)

        self.process_queue = Queue()

    def append(self, process):
        self.process_queue.put(process)

    def dispatch(self):
        if self.process_queue.empty():
            return None
        else:
            return self.process_queue.get()

    def run_until_complete(self):
        """
            currrent_process   : 调度之后获得的当前要执行的任务
            current_time       : 当前时刻，不停运行同时不停更新，在不同的时间载入不同的任务
        """
        current_time = 0
        current_process = None

        while self.process_unloaded or self.process_in_memory:  # 只要还有进程在内存或者没载入就一直进行下去
            while self.process_unloaded:  # 如果还有没载入的进程
                first_process = self.process_unloaded[0]
                if first_process.reachTime == current_time:
                    # 如果进程可以载入就载入
                    self.process_in_memory.add(first_process)
                    self.process_queue.put(first_process)
                    self.process_unloaded.pop(0)
                elif first_process.reachTime > current_time:
                    break

            if current_process:
                if current_process.is_complete():
                    # 如果当前运行的进程存在且结束了，那就将这个进程弹出内存
                    self.process_in_memory.remove(current_process)
                    current_process = self.dispatch()
            else:
                # 如果没有当前运行的进程就调度一个
                current_process = self.dispatch()

            if current_process:  # 有进程就运行1个gap
                current_process.run(1)

            self.update(1)

            current_time += 1

    def load(self, filename):
        with open(filename, 'r') as f:
            process_lines = [line for line in f.read().split('\n') if line.strip()]
            for process_line in process_lines:
                process_info = process_line.split()
                process = Process(*process_info)
                self.process_unloaded.append(process)

    def analysis(self):
        total_wait_time = sum(self.process_wait_time.values())
        process_number = len(self.process_wait_time)
        average = total_wait_time / process_number

        for process, wait_time in self.process_wait_time.items():
            print("{}\twait for : {}".format(process, wait_time))
        print("-" * 20)
        print("FCFS Complete. Average turnaround time : {}".format(average))

    def update(self, time):
        for process in self.process_in_memory:
            self.process_wait_time[process] += time

    def reorder(self):
        """FCFS不需要对进程队列重新排序"""
