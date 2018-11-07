from . import Page


class Process:
    def __init__(self, memory_needed, *address_used):
        """

        :param memory_needed: 需要使用的总内存，是4096的倍数，用来计算需要的页数
        :param address_used: 使用地址号的序列，不维护时间
            page_number: 页数，由memory_needed算得
            pages: 所有的页
        """
        self.memory_needed = memory_needed

        self.page_number = self.memory_needed // 4096
        self.address_used = address_used
        self.pages = [
            Page() for _ in range(self.page_number)
        ]
