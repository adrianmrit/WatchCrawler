import argparse
from load import load_data
from scrapy.crawler import CrawlerProcess
from watches import crawler_creator
import json
from scrapy.utils.project import get_project_settings


def parse_watch_store(self, response):
    """Save watch from a store page using save(watch)

    Arguments:
        response {scrapy.http.Response} -- response object
    """
    watch = {}
    print(response.request.headers)
    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])

    save_watch(watch)


def parse_watch_brand(self, response):
    """Save a watch from the brand page using save_watch(watch)

    Arguments:
        response {scrapy.http.Response} -- response object
    """
    watch = {}

    # url and brand are not extracted from the page in this case
    watch['url'] = response.url
    watch['brand'] = self.params['brand']

    for field in self.params['xpaths'].keys():
        watch[field] = get_field(response, self.params['xpaths'][field])

    save_watch(watch)


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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap data from only one website')
    parser.add_argument('--file', metavar='path', required=True,
                        help='the path to the json file')
    args = parser.parse_args()

    page_struct = load_data([args.file])[0]
    process = CrawlerProcess(get_project_settings())

    if page_struct['type'] == 'brand':
        process.crawl(crawler_creator(page_struct, parse_watch_brand))
    elif page_struct['type'] == 'store':
        process.crawl(crawler_creator(page_struct, parse_watch_store))

    process.start()