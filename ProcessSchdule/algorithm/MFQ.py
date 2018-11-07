from collections import defaultdict
from queue import Queue
from model.Process import Process


class queue:
    base_chip = 25

    def __init__(self, level, lowest=False):
        """

        :param level: 队列的等级
        :param lowest:  队列是否已经是最底层队列
                q: 真正的队列
                process_chip_unifnished: 高优先级进程进入之后直接切换到高优先级进程，然后将当前还剩下的时间片记录下来，下次直接分配这个时间片
        """
        self.level = level
        self.lowest = lowest
        self.q = Queue()
        self.process_chip_unfinished = {}

    def put(self, process):
        self.q.put(process)

    def get(self):
        return self.q.get()

    def empty(self):
        return self.q.empty()

    @property
    def chip(self):
        return self.base_chip * self.level

    def is_lowest(self):
        return self.lowest

    def record_chip_unfinished(self, process, time):
        self.process_chip_unfinished[process] = time

    def clear_chip_unfinished(self, process):
        if process in self.process_chip_unfinished:
            self.process_chip_unfinished.pop(process)


class Scheduler:
    def __init__(self):
        """
            process_unload     : 已经按照到达时间排序好的所有进程信息，还没有载入到内存中，每次载入一个则弹出一个
            process_in_memory  : 已经载入到内存的进程，这部分进程需要计算等待时间，进程执行完毕需要弹出，所以没有使用列表
            process_wait_time  : 每个进程的周转时间
            current_process    : 当前执行的进程

            qs                 : 所有的队列
            current_queue      : 当前执行的进程所在的队列
            current_queue_index: 当前队列在所有队列中的索引

        chip        : 分配的时间片
        chip_set_up : 是否分配了时间片
        """
        self.process_unloaded = []
        self.process_in_memory = set()
        self.process_wait_time = defaultdict(int)
        self.current_process = None

        self.qs = [
            queue(1),
            queue(2),
            queue(3, True)
        ]
        self.current_queue = None
        self.current_queue_index = None
        self.chip = 0
        self.chip_set_up = False

    def run_until_complete(self):
        current_time = 0

        while self.process_unloaded or self.process_in_memory:  # 只要还有进程在内存或者没载入就一直进行下去
            while self.process_unloaded:  # 如果还有没载入的进程
                first_process = self.process_unloaded[0]
                if first_process.reachTime == current_time:
                    # 如果进程可以载入就载入
                    self.process_in_memory.add(first_process)
                    self.append(first_process)
                    self.process_unloaded.pop(0)
                elif first_process.reachTime > current_time:
                    break

            if self.current_process:
                if self.current_process.is_complete():
                    #  如果当前运行的进程存在且结束了，那就将这个进程弹出内存
                    self.process_in_memory.remove(self.current_process)
                    self.current_process = self.dispatch()
                elif self.chip == 0 and self.chip_set_up:
                    # 如果设置了时间片且时间片归零了进程还没运行完
                    self.current_queue.clear_chip_unfinished(self.current_process)
                    if self.current_queue.is_lowest():
                        # 如果已经是最底层的队列了
                        self.current_queue.put(self.current_process)
                    else:
                        next_queue = self.qs[self.current_queue_index + 1]
                        next_queue.put(self.current_process)
                    self.current_process = self.dispatch()
            else:
                self.current_process = self.dispatch()

            if self.current_process:  # 有进程就运行1个gap
                self.current_process.run(1)
                self.chip -= 1

            self.update(1)

            current_time += 1

    def dispatch(self):
        """
        进行调度，返回第一个
        """
        for index, q in enumerate(self.qs):
            if not q.empty():
                process = q.get()
                self.current_queue = q
                self.current_queue_index = index
                if process in q.process_chip_unfinished:
                    self.set_chip(q.process_chip_unfinished[process])
                else:
                    self.set_chip(q.chip)
                return process
        return None

    def append(self, process):
        """
        :param process: 在进程组中添加一个进程
        """
        if self.current_queue is None or self.current_queue.level > self.qs[0].level:
            # 如果有低优先级队列在执行
            if self.current_queue:
                # 如果有低优先级程序正在执行，记录时间片，并切换进程（开销1）
                self.current_queue.record_chip_unfinished(self.current_process, self.chip)
                self.update(1)

            # 如果是直接切换进程，那就不将进程放入队列中，直接切换过去就好
            self.current_process = process
            self.current_queue = self.qs[0]
            self.current_queue_index = 0
        else:
            # 否则就放入进程队列中
            self.qs[0].put(process)

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

    def set_chip(self, chip):
        """
        :param chip: 要分配的时间片
        """
        self.chip = chip
        self.chip_set_up = True

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

        print("{} Complete. Average turnaround time : {}ms".format(name, average))
