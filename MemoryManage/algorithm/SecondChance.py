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
            SecondChance每次从页框队列中遍历，如果队头的页框对应的页访问位为0，则将这个页框对应的页置换出去，否则就将这个页访问位置为0，继续遍历
        :param page: 要置换进内存的页面
        """
        while 1:
            page_frame_replaced = self.page_frame_queue.get()
            self.page_frame_queue.put(page_frame_replaced)

            old_page = page_frame_replaced.page
            if old_page is None or old_page.referenced == 0:
                if old_page:
                    old_page.reset()

                page_frame_replaced.page = page
                page.page_frame = page_frame_replaced
                page.exist = 1
                break
            else:
                old_page.referenced = 0

    def use(self, page):
        """每次访问之后将页面的访问位置1"""
        page.referenced = 1
