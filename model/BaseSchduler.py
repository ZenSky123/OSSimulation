class BaseSchduler:
    def append(self, task):
        """给任务队列中添加一个任务"""

    def dispatch(self):
        """"进行调度，选择下一个要执行的程序"""

    def run_until_complete(self):
        """不停地执行程序、调度、执行程序，直到全部程序执行完毕"""

    def load(self, filename):
        """从文件中加载进程组的数据"""

    def reorder(self):
        """对进程组重新排序"""

    def update(self, time):
        """给予一个时间参数，然后更新其他进程的统计信息"""
