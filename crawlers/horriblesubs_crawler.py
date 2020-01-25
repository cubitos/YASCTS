#! /usr/bin/env python 

from crawlers.base_crawler import BaseCrawler
from lxml import html
import urllib.request
import ssl

class HorribleSubsCrawler(BaseCrawler):
    """
    A crawler for horriblesubs database. 
    """

    def __init__(self):
        self.homepage = "https://horriblesubs.info/shows"
        pass

    def crawl(self):
        page = html.fromstring(BaseCrawler.parse_url(self.homepage))
        for item in page.xpath("//div[@class='ind-show']/a"):
            text = item.text.strip()
            print(text)