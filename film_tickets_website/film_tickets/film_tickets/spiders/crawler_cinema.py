# -*- coding: utf-8 -*-
import scrapy


class CrawlerCinemaSpider(scrapy.Spider):
    name = 'crawler_cinema'
    allowed_domains = ['www.taopiaopiao.com']
    start_urls = ['https://www.taopiaopiao.com/showList.htm?spm=a1z21.6646273.city.3.3558c6fdo4UxCB&n_s=new']

    def parse(self, response):
        pass
