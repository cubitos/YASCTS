#! /usr/bin/env python 
from lxml import html
import urllib.request
import ssl
from yamlable import yaml_info, YamlAble

@yaml_info(yaml_tag_ns='com.cubitos.BaseDownloadableItem')
class BaseDownloadableItem(YamlAble):
    def get_task(self):
        pass

@yaml_info(yaml_tag_ns='com.cubitos.BaseShow')
class BaseShow(YamlAble):
    def populate(self):
        pass

@yaml_info(yaml_tag_ns='com.cubitos.BaseCrawler')
class BaseCrawler(YamlAble):
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

    def populate(self, index):
        pass

    def save(self, filename):
        pass

    @staticmethod
    def load(filename):
        pass