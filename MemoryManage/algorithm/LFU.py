from model import BaseMMU


class MMU(BaseMMU):
    def __init__(self, memory_size):
        """

        :param memory_size: 内存大小
            page_frame_queue 页框号的队列，里面只存页框号(int)
        """
        super().__init__(memory_size)
        for page_frame in self.page_frames:
            page_frame.count = 0
            # 给每个页框增加一个count值，设置为访问次数

    def replace(self, page):
        """
            LRU算法给每个页框维护一个count值，被访问的次数，每次取被访问次数最小的页框置换出去
        :param page: 要置换进内存的页面
        """
        page_frame_replaced = min(self.page_frames, key=lambda page_frame: page_frame.count)  # 获取访问次数最小的页框
        old_page = page_frame_replaced.page
        if old_page is not None:
            old_page.reset()

        page_frame_replaced.count = 1
        page_frame_replaced.page = page
        page.exist = 1
        page.page_frame = page_frame_replaced

    def use(self, page):
        """每次访问之后将页框的访问次数加1"""
        page.page_frame.count += 1
