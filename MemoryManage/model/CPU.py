from . import Process
import random


class CPU:
    def __init__(self, MMU):
        """

        :param MMU: CPU要向MMU发送取地址指令
            processes: CPU要执行的所有进程
            process_address_use: 二元组列表，Ex: [(Process0,23),(Process3,5000)] 意为依次进程0访问地址23，进程3访问地址5000

            page_break: 缺页中断数
            page_hit:   页面命中数
        """
        self.MMU = MMU
        self.processes = []
        self.process_address_use = []
        self.load()

        self.page_break = 0
        self.page_hit = 0

    def use(self, process, address):
        """
        向MMU发送取地址指令
        :param process: 使用内存的进程
        :param address: 要使用的地址号
        """
        address_page_index = address // 4096  # 对应的进程的页表项
        address_page = process.pages[address_page_index]

        if not address_page.exist:
            self.MMU.replace(address_page)
            self.page_break += 1
        else:
            self.page_hit += 1
        self.MMU.use(address_page)

    def run_until_complete(self):
        [self.use(process, address_use) for process, address_use in self.process_address_use]

    def load(self, filename='default.dat'):
        """
        将文件数据加载到processes和process_address_use两个列表中
        :param filename: 要加载的数据文件名
        """
        filepath = 'data/{}'.format(filename)
        with open(filepath) as f:
            for line in [line for line in f.read().split('\n') if line.strip()]:
                line_data = list(map(int, line.split()))
                process = Process(*line_data)
                self.processes.append(process)
                for address_use in process.address_used:
                    self.process_address_use.append((process, address_use))
        random.shuffle(self.process_address_use)

    def analysis(self, func_name):
        print(func_name, ":")
        print('\t', 'page_break : {}'.format(self.page_break))
        print('\t', 'page_hit : {}'.format(self.page_hit))
        print("-" * 30)
