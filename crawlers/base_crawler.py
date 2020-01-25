#! /usr/bin/env python 
from lxml import html
import urllib.request
import ssl
class BaseCrawler:
    """
    A base crawler is a minimal definition on what is to be explored in order to get tasks
    """

    def __init__(self):
        pass

    @staticmethod
    def parse_url(url:str) -> str:
        request = urllib.request.Request(url=url, headers={'User-Agent':'Mozilla/5.0'})
        return urllib.request.urlopen(request).read()

    def crawl(self):
        pass