from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from load import load
from WatchSpider.items import Watch
import json
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

config = json.load(open('config.json'))


def get_field(response, xpath):
    """Get field using xpath"""
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()

    return None

def parse_image_url(url):
    parsed = urllib.parse.urlparse(url)
    url = ''
    if not parsed.scheme:
        url+="http://"
    else:
        url+=parsed.scheme
    url += parsed.netloc
    url += parsed.path

    if parsed.query:
        url += "?"
        url += parsed.query

    return url

def save_watch(watch):
    url = parse_image_url(watch['image'])
    image = requests.get(url)
    del watch['image']
    img = Image.open(BytesIO(image.content))
    byte_io = BytesIO()
    img.save(byte_io, 'JPEG')
    files = {'image': (watch['reference']+watch['name']+".jpg", byte_io.getvalue(), "image/jpeg")}


    response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})


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