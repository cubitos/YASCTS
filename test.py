#! /usr/bin/env python 

from crawlers.horriblesubs_crawler import HorribleSubsCrawler

c = HorribleSubsCrawler()
#c = HorribleSubsCrawler.load()
c.crawl() # crawls base index
c.populate(1) # populate show 1 - on demand, iterate for more
c.populate(10) # populate show 10