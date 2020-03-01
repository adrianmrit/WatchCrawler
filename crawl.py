from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from load import load


process = CrawlerProcess()

data = load('data')

for brand in data:
    process.crawl(crawler_creator(brand))

process.start()