from model import BaseMMU
import time


class MMU(BaseMMU):
    def __init__(self, memory_size):
        """

        :param memory_size: 内存大小
            page_frame_queue 页框号的队列，里面只存页框号(int)
        """
        super().__init__(memory_size)
        for page_frame in self.page_frames:
            page_frame.last_visit_time = time.time()
            # 给每个页框增加一个last_visit_time值，设置为上次访问的次数

    def replace(self, page):
        """
            LRU算法给每个页框维护一个time值，上次访问的时间，每次取上次被访问时间最远的页框置换出去
        :param page: 要置换进内存的页面
        """
        page_frame_replaced = min(self.page_frames, key=lambda page_frame: page_frame.last_visit_time)  # 获取上次访问时间最远的框
        old_page = page_frame_replaced.page
        if old_page is not None:
            old_page.reset()

        page_frame_replaced.last_visit_time = time.time()
        page_frame_replaced.page = page
        page.exist = 1
        page.page_frame = page_frame_replaced

    def use(self, page):
        """每次访问之后将页面的上次访问时间置为当前时间"""
        page.page_frame.last_visit_time = time.time()
