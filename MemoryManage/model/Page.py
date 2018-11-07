class Page:
    def __init__(self):
        """
            cache_forbidden 缓存禁止位
            protection 保护位
            modified 修改位
            referenced 访问位
            exist 在/不在位
            page_frame_index 页框号
        """
        self.cache_forbidden = 0
        self.protection = 0
        self.modified = 0
        self.referenced = 0
        self.exist = 0
        self.page_frame_index = None

    def reset(self):
        """
            重置页，为简化模型，略去了修改位为1的处理情况，只简单的将页框号置为None
        """
        self.__init__()


class PageFrame:
    def __init__(self):
        """
            page 页框对应的页
        """
        self.page = None  # 默认没有对应的页
