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
    """Get a field using xpath

    Arguments:
        response {scrapy.http.Response} -- response object
        xpath {string} -- xpath to the field

    Returns:
        [string] -- xpath match
    """
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()  # TODO: clean data even further

    return None


def clean_url(url):
    """Clean any url, specially useful for those starting with double slash

    Arguments:
        url {string} -- [Url to be cleaned]

    Returns:
        [string] -- [cleaned url]
    """
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
    """Upload the watch data using the api.

    Arguments:
        watch {dict} -- Watch to be saved.
    """
    if watch['reference']:  # ?if there is no reference probably it wasn't a watch
        url = clean_url(watch['image'])

        image = requests.get(url)
        del watch['image']  # avoid uploading image as a field

        img = Image.open(BytesIO(image.content))
        byte_io = BytesIO()
        img.save(byte_io, 'JPEG')
        image_name = watch['reference'] + watch['name'] + ".jpg"
        files = {'image': (image_name, byte_io.getvalue(), "image/jpeg")}

        # TODO: use json instead of data
        response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})


def parse_watches(self, response):
    """Callback function to parse the watches

    Arguments:
        response {Scrapy Response} -- Scrapy Response object that will be processed
    """
    watch = {}

    watch['url'] = response.url
    watch['brand'] = self.params['brand']  # each crawler object has this

    # Use the same xpath fields in params['xpaths'] as in the watch dict. This field MUST be the same as in the api
    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])

    save_watch(watch)


if __name__ == '__main__':
    process = CrawlerProcess()

    data = load('data')


    # creates a crawler for each brand.
    for brand in data:
        process.crawl(crawler_creator(brand, parse_watches))

    process.start()