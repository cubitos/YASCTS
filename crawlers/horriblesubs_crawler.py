#! /usr/bin/env python 

from pathlib import Path
from crawlers.base_crawler import BaseCrawler, BaseDownloadableItem, BaseShow
from lxml import html, etree
import re
import urllib.request
import ssl
import yaml
from yamlable import yaml_info, YamlAble

@yaml_info(yaml_tag_ns='com.cubitos.HorriblesubsDownloadableItem')
class HorriblesubsDownloadableItem(BaseDownloadableItem):
    def __init__(self, index="", container="", download_type="", url=""):
        self.index = index
        self.container = container
        self.download_type = download_type
        self.url = url

@yaml_info(yaml_tag_ns='com.cubitos.HorribleSubsShow')
class HorriblesubsShow(BaseShow):
    def __init__(self, title="", show_page="", show_id="", items=[]):
        self.title = title
        self.show_page = show_page
        self.show_id = show_id
        self.items = items

    def inject_show_id(self):
        if len(self.show_id) == 0:
            site_html = BaseCrawler.parse_url(self.show_page)
            page = html.fromstring(site_html)
            for item in page.xpath("//div[@class='entry-content']/script[@type='text/javascript']"):
                show_text = item.text.strip()
                show_id = re.findall(r"\d+", show_text)[0]
                self.show_id = show_id

    def populate(self):
        self.inject_show_id()
        self.populate_downloadable_index(index_type="show")
        self.populate_downloadable_index(index_type="batch")

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
                    link_type = str(download_item.text_content())
                    if(len(link_type) > 3):
                        link_url = download_item.get("href")
                        if not any(x.url == link_url for x in  self.items):
                            self.items.append(HorriblesubsDownloadableItem(ep_index, container_type, link_type, link_url))
                            print(ep_index, container_type, link_type)
            
    
@yaml_info(yaml_tag_ns='com.cubitos.HorribleSubsCrawler')
class HorribleSubsCrawler(BaseCrawler):
    """
    A crawler for horriblesubs database. 
    """

    def __init__(self, base_address = "https://horriblesubs.info", shows_address = "/shows", shows = []):
        self.base_address = base_address
        self.shows_address = shows_address
        self.shows = shows

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
                self.shows.append(HorriblesubsShow(title=text, show_page=page))

    def save(self, filename="./database/horriblesubs.yml"):
        dump_file = open(filename, "w")
        dump_file.write(yaml.dump(self))
        dump_file.close()

    @staticmethod
    def load(filename="./database/horriblesubs.yml"):
        return yaml.safe_load(Path(filename).read_text())

    def populate(self, index = None):
        self.shows[index].populate()
        self.save()

    def crawl(self):
        self.populate_shows_index()
        #self.shows[1].populate()
        #for x in self.shows[0].items:
            #print(x)
        self.save()
        #self.shows[0].populate_downloadable_index()