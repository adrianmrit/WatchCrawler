from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from load import load
from WatchSpider.items import Watch
import json

def get_field(response, xpath):
    """Get field using xpath"""
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()

    return None


def save_watch(watch):
    with open('results/' + watch['reference'] + '.json', 'w') as fp:
                json.dump(dict(watch), fp, indent=4)


def parse_watches(self, response):
            watch = Watch()

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