from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WatchSpider.items import Watch
import json


def get_field(response, xpath):
    """If no xpath return empty"""
    if xpath:
        return response.xpath(xpath).get()
    else:
        return None


def save_watch(watch):
    with open('results/' + watch['reference'] + '.json', 'w') as fp:
                json.dump(dict(watch), fp, indent=4)


# TODO: clean spaces from data
# TODO: remember to use refer
def crawler_creator(params):
    """Generate a crawler with params"""

    class Crawler(CrawlSpider):
        name = params['brand']
        allowed_domains = params['allowed_domains']
        start_urls = params['start_urls']

        custom_settings = {
            'DOWNLOAD_DELAY': 3,
        }


        # ! if no suplied empty array to allow in LinkExtractor it will follow all links. To fix this use r"\b\B", wich wont match anything.
        allowed_collections_urls = r"\b\B"
        if params['allowed_collections_urls']:
            allowed_collections_urls = params['allowed_collections_urls']

        rules = [
            Rule(LinkExtractor(allow=allowed_collections_urls), follow=True),
            Rule(LinkExtractor(allow=params['allowed_watches_urls']), callback='parse_watches', follow=False)]


        def parse_watches(self, response):
            watch = Watch()

            watch['url'] = response.url
            watch['brand'] = params['brand']

            for field in params['xpaths'].keys():
                watch[field] = get_field(response, params['xpaths'][field])

            save_watch(watch)

    print('Created Crawler')
    return Crawler