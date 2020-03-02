from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from load import load
from WatchSpider.items import Watch
import json
import requests

config = json.load(open('config.json'))


def get_field(response, xpath):
    """Get field using xpath"""
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()

    return None


def save_watch(watch):
    response = requests.post(config['server'], json=watch, headers={'Authorization':config['auth_token']})


def parse_watches(self, response):
            watch = {}

            watch['url'] = response.url
            watch['brand'] = self.params['brand']

            for field in self.params['xpaths'].keys():
                watch[field] = get_field(response, self.params['xpaths'][field])

            save_watch(watch)

process = CrawlerProcess()

data = load('data')

for brand in data:
    process.crawl(crawler_creator(brand, parse_watches))

process.start()