from enum import Enum


class State(Enum):
    Execute = 1
    Ready = 2
    Complete = 3


class Process:
    def __init__(self, pid, reachTime, needTime, priority):
        """
        :param pid: 进程ID
        :param reachTime: 进程到达时间
        :param needTime: 进程总共所需时间
        :param priority: 优先级
                cputime: 进程已经占用的时间
                alltime: 进程还需执行的时间（执行完毕的时候这个值为0）
                state: 进程的状态，E为执行，R为就绪，F为完成
        """

        self.pid = pid
        self.reachTime = int(reachTime)
        self.needTime = int(needTime)
        self.priority = int(priority)

        self.cputime = 0
        self.alltime = int(needTime)
        self.state = State.Ready

    def __str__(self):
        return "[Process PID/Priority/needed : {}/{}/{} ]".format(self.pid, self.priority, self.needTime)

    def run(self, time):
        """
            让进程执行对应时间
            进程是否结束在调度器处检测
        """
        self.alltime -= time
        self.cputime += time

        if self.alltime == 0:
            self.switch_to_complete()

    def switch_to_complete(self):
        """切换到完成状态"""
        self.state = State.Complete

    def switch_to_ready(self):
        """切换到就绪状态"""
        self.state = State.Ready

    def switch_to_execute(self):
        """切换到执行状态"""
        self.state = State.Execute

    def is_complete(self):
        """是否进程已经结束"""
        return self.state is State.Complete

    def set_priority(self, priority):
        """设置优先级"""
        self.priority = priority
