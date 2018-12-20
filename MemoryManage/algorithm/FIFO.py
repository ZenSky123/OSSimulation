from model import BaseMMU
from queue import Queue


class MMU(BaseMMU):
    def __init__(self, memory_size):
        """

        :param memory_size: 内存大小
            page_frame_queue 页框号的队列，里面只存页框号(int)
        """
        super().__init__(memory_size)
        self.page_frame_queue = Queue()
        [self.page_frame_queue.put(page_frame) for page_frame in self.page_frames]

    def replace(self, page):
        """
            FIFO算法每次从页框队列中取出一个最老的将页面映射到这个页框
        :param page: 要置换进内存的页面
        """
        page_frame_replaced = self.page_frame_queue.get()
        self.page_frame_queue.put(page_frame_replaced)

        old_page = page_frame_replaced.page
        if old_page is not None:
            old_page.reset()

        page_frame_replaced.page = page
        page.page_frame = page_frame_replaced
        page.exist = 1

    def use(self, page):
        """FIFO算法在使用完一个页面之后不需要对队列做更新"""
