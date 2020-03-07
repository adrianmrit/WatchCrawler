from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from WatchSpider import settings as global_settings


def get_field(response, xpath):
    """Get a field using xpath

    Arguments:
        response {scrapy.http.Response} -- response object
        xpath {string} -- x

    Returns:
        [string] -- xpath match
    """
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()
        else:
            with open('xpath_logs.txt', 'a') as logfile:
                logfile.write(xpath + '---' + response.url + '\n\n')

    return None


def save_watch(watch):
    with open('results/' + watch['reference'] + '.json', 'w') as fp:
                json.dump(dict(watch), fp, indent=4)


def crawler_creator(params, watch_parser):
    """Generate a Crawler for different pages.

    Arguments:
        params {dict} -- see base.json for example
        watch_parser {function} -- call back function for links that match allowed watches url

    Returns:
        Crawler -- Crawler object used by scrapy
    """

    class Crawler(CrawlSpider):
        def __init__(self, *a, **kw):
            self.params = params
            self.name = params['allowed_domains'][0]
            self.allowed_domains = params['allowed_domains']
            self.start_urls = params['start_urls']

            # ! if no suplied empty array to allow in LinkExtractor it will follow all links. To fix this use r"\b\B", wich wont match anything.
            allowed_collections_urls = r"\b\B"
            if self.params['allowed_collections_urls']:
                allowed_collections_urls = self.params['allowed_collections_urls']

            self.rules = [
                Rule(LinkExtractor(allow=allowed_collections_urls), follow=True),
                Rule(LinkExtractor(allow=self.params['allowed_watches_urls']), callback='parse_watches', follow=False)]

            Crawler.parse_watches = watch_parser
            super().__init__(*a, **kw)


    return Crawler