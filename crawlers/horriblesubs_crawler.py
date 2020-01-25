#! /usr/bin/env python 

from crawlers.base_crawler import BaseCrawler
from lxml import html, etree
import re
import urllib.request
import ssl

class HorriblesubsDownloadableItem:
    def __init__(self, index="", container="", download_type="", url=""):
        self.index = index
        self.container = container
        self.download_type = download_type
        self.url = url

class HorriblesubsShow:
    def __init__(self, title="", page=""):
        self.title = title
        self.show_page = page
        self.show_id = ""
        self.items = []

        # Should be outside trigger
        self.inject_show_id()
        self.populate_downloadable_index(index_type="show")
        self.populate_downloadable_index(index_type="batch")

    def inject_show_id(self):
        site_html = BaseCrawler.parse_url(self.show_page)
        page = html.fromstring(site_html)
        for item in page.xpath("//div[@class='entry-content']/script[@type='text/javascript']"):
            show_text = item.text.strip()
            show_id = re.findall(r"\d+", show_text)[0]
            self.show_id = show_id


    def populate_downloadable_index(self, index_type='show'):
        page = html.fromstring(HorribleSubsCrawler.call_api({
            'method':'getshows',
            'type':index_type,
            'showid': self.show_id
        }))

        for item in page.xpath("//div[@class='rls-info-container']"):
            ep_index = item.xpath("a/strong")[0].text.strip() 
            for container in item.xpath("div[contains(@class, 'rls-links-container')]/div"):
                container_type = container.xpath("span[@class='rls-link-label']")[0].text.strip().replace(":", "")
                for download_item in container.xpath("span[contains(@class, 'dl-type')]/a"):
                    link_type = download_item.text_content()
                    if(len(link_type) > 3):
                        link_url = download_item.get("href")
                        self.items.append(HorriblesubsDownloadableItem(ep_index, container_type, link_type, link_url))
            
    

class HorribleSubsCrawler(BaseCrawler):
    """
    A crawler for horriblesubs database. 
    """

    def __init__(self):
        self.base_address = "https://horriblesubs.info"
        self.shows_address = "/shows"
        self.shows = []
        pass

    @staticmethod
    def call_api(params:dict):
        base_url = "https://horriblesubs.info/api.php"
        parameter_map = []
        for k,v in params.items():
            parameter_map.append(k + "=" + v)
        parameter_map = "&".join(parameter_map)
        url = "?".join([base_url, parameter_map])
        return BaseCrawler.parse_url(url)
        

    def populate_shows_index(self):
        page = html.fromstring(BaseCrawler.parse_url(self.base_address + self.shows_address))
        for item in page.xpath("//div[@class='ind-show']/a"):
            text = item.text.strip()
            page = self.base_address + item.get("href")
            if not any(x.show_page == page for x in  self.shows):
                self.shows.append(HorriblesubsShow(title=text, page=page))

            ## Remove after test
            return

    def crawl(self):
        print(self.shows[0].title)
        print(self.shows[0].show_page)
        print(self.shows[0].show_id)
        for x in self.shows[0].items:
            print(x)
        #self.shows[0].populate_downloadable_index()