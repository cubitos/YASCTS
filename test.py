#! /usr/bin/env python 

from crawlers.horriblesubs_crawler import HorribleSubsCrawler

c = HorribleSubsCrawler()
c.populate_shows_index()
c.crawl()