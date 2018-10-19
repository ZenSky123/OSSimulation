from collections import defaultdict

from model.Process import Process


class BaseSchduler:
    def __init__(self):
        """
        process_unload     : 已经按照到达时间排序好的所有进程信息，还没有载入到内存中，每次载入一个则弹出一个
        process_in_memory  : 已经载入到内存的进程，这部分进程需要计算等待时间，进程执行完毕需要弹出，所以没有使用列表
        process_wait_time  : 每个进程的周转时间
        process_candidate  : 进程候选列表，dispatch函数通过这个列表来实现调度

        chip        : 分配的时间片
        chip_set_up : 是否分配了时间片
        """
        self.process_unloaded = []
        self.process_in_memory = set()
        self.process_wait_time = defaultdict(int)
        self.process_candidate = []

        self.chip = 0
        self.chip_set_up = False

    def append(self, process):
        """
        :param process: 要添加的进程
        给任务队列中添加一个任务，添加完之后要对候选进程组进行重新排序，将下一次调度获得的程序放到列表首位
        """
        self.process_candidate.append(process)
        self.reorder()

    def run_until_complete(self):
        """
        不停地执行程序、调度、执行程序，直到全部程序执行完毕
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
                    self.process_candidate.append(first_process)
                    self.process_unloaded.pop(0)
                elif first_process.reachTime > current_time:
                    break

            if current_process:
                if current_process.is_complete():
                    #  如果当前运行的进程存在且结束了，那就将这个进程弹出内存
                    self.process_in_memory.remove(current_process)
                    current_process = self.dispatch()
                elif self.chip == 0 and self.chip_set_up:
                    # 如果设置了时间片且时间片归零了进程还没运行完，将刚才的进程重新放进候选队列
                    # 强制进行调度
                    self.append(current_process)
                    current_process = self.dispatch()
            else:
                # 如果没有当前运行的进程就调度一个
                current_process = self.dispatch()

            if current_process:  # 有进程就运行1个gap
                current_process.run(1)
                self.chip -= 1

            self.update(1)

            current_time += 1

    def load(self, filename):
        """
        :param filename: 文件名
        通过文件读取数据
        """
        with open(filename, 'r') as f:
            process_lines = [line for line in f.read().split('\n') if line.strip()]
            for process_line in process_lines:
                process_info = process_line.split()
                process = Process(*process_info)
                self.process_unloaded.append(process)

    def update(self, time):
        """
        :param time:时间参数
        给予一个时间参数，然后更新其他进程的统计信息
        """
        for process in self.process_in_memory:
            self.process_wait_time[process] += time

    def analysis(self, name):
        """
        :param name: 调度算法名字
        """
        total_wait_time = sum(self.process_wait_time.values())
        process_number = len(self.process_wait_time)
        average = total_wait_time / process_number

        # 输出每一个进程的等待时间
        # for process, wait_time in self.process_wait_time.items():
        #     print("{}\twait for : {}".format(process, wait_time))

        print("{} Complete. Average turnaround time : {}".format(name, average))

    def set_chip(self, chip):
        """
        :param chip: 要分配的时间片
        """
        self.chip = chip
        self.chip_set_up = True

    def dispatch(self):
        """"进行调度，选择下一个要执行的程序"""

    def reorder(self):
        """对进程组重新排序"""
