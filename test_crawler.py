import argparse
from load import load_data
from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
from WatchSpider.items import Watch
import json


# TODO: save images locally
def get_field(response, xpath):
    """Get field and log broken xpaths"""
    if xpath:
        field = response.xpath(xpath).get()
        if field:
            return field.strip()
        else:
            with open('xpath_logs.txt', 'a') as logfile:
                logfile.write(xpath + '---' + response.url + '\n\n')

    return None


def save_watch(watch):
    """Save watch as json"""
    with open('results/' + watch['reference'] + '.json', 'w') as fp:
                json.dump(dict(watch), fp, indent=4)



def parse_watches(self, response):
    """Save a watch using save_watch(watch)

    Arguments:
        response {scrapy.http.Response} -- response object
    """
    watch = Watch()

    watch['url'] = response.url
    watch['brand'] = self.params['brand']

    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])

        save_watch(watch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap data from only one website')
    parser.add_argument('--file', metavar='path', required=True,
                        help='the path to the json file')
    args = parser.parse_args()

    brand = load_data([args.file])[0]

    process = CrawlerProcess()
    process.crawl(crawler_creator(brand, parse_watches))
    process.start()