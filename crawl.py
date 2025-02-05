from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from load import load
import json
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
from scrapy.utils.project import get_project_settings
from utils.urls import clean_url
from utils.images import load_img_from_request

PROJECT_SETTINGS = get_project_settings()

HEADERS = {'User-Agent': get_project_settings()['USER_AGENT']}  # headers to use with non scrapy requests
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


def save_watch(watch):
    """Upload the watch data using the api.

    Arguments:
        watch {dict} -- Watch to be saved.
    """
    if watch['reference']:  # ?if there is no reference probably it wasn't a watch
        url = watch['image']

        image = requests.get(url, headers=HEADERS)
        del watch['image']  # avoid uploading image as a field

        image = load_img_from_request(image)
        image_name = watch['reference'] + watch['name'] + ".jpg"  # TODO: Clean reference and name from slashes and other
        files = {'image': (image_name, image, "image/jpeg")}

        # TODO: use json instead of data
        response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})


def parse_watch_brand(self, response):
    """Callback function to parse the watches

    Arguments:
        response {Scrapy Response} -- Scrapy Response object that will be processed
    """
    watch = {}

    # Use the same xpath fields in params['xpaths'] as in the watch dict. This field MUST be the same as in the api
    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])


    watch['url'] = response.url
    watch['brand'] = self.params['brand']
    watch['image'] = clean_url(watch['image'])
    watch['store'] = self.params['brand']
    watch['sale_url'] = response.url
    watch['currency'] = self.params['default_currency']
    save_watch(watch)


def parse_watch_store(self, response):
    """Save watch from a store page using save(watch)

    Arguments:
        response {scrapy.http.Response} -- response object
    """
    watch = {}
    print(response.request.headers)
    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])

    watch['image'] = clean_url(watch['image'])
    watch['store'] = self.params['store']
    watch['sale_url'] = response.url
    watch['currency'] = self.params['default_currency']
    save_watch(watch)


if __name__ == '__main__':
    process = CrawlerProcess(PROJECT_SETTINGS)  # set global settings

    data = load('data')


    # create the correct crawler for each type of site
    for page_struct in data:
        if page_struct['type'] == 'store':
            process.crawl(crawler_creator(page_struct, parse_watch_store))
        elif page_struct['type'] == 'brand':
            process.crawl(crawler_creator(page_struct, parse_watch_brand))

    process.start()