from cinema_spider.utils import get_line_name


class City:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('nm')
        self.pinyin = kwargs.get('py')
        self.line_name = get_line_name(self.pinyin)
        self.brand = kwargs.get('brand')
