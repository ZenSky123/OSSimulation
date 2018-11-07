from . import PageFrame


class BaseMMU:
    def __init__(self, memory_size):
        """
        :param memory_size:内存空间大小
                page_frame_number MMU中的页框数
                page_frames MMU中的所有页框
        """
        self.page_frame_number = memory_size // 4096
        self.page_frames = [
            PageFrame() for _ in range(self.page_frame_number)
        ]

    def replace(self, page):
        """
        将不在内存中的页page置换到内存中并更新页和页框的映射信息
        :param page: 不在内存中的页
        """

    def use(self, page):
        """
        通过这个页来映射到要使用的页框，然后更新页框相关信息，供页面置换算法使用
        同时这个过程就等同于现实中从物理地址中取到目标值的过程
        :param page: 要使用的地址所在的页
        """
