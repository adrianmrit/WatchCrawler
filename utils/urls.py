import urllib.parse
import re

def clean_url(url):
    """Clean any url, specially useful for those starting with double slash

    Arguments:
        url {string} -- [Url to be cleaned]

    Returns:
        [string] -- [cleaned url]
    """
    if url:
        url = url.replace('\\', '')  # TODO: better clean
        parsed = urllib.parse.urlparse(url)
        url = ''

        if not parsed.scheme:
            url += "http://"
        else:
            url += parsed.scheme + "://"

        url += parsed.netloc
        url += parsed.path

        if parsed.query:
            url += "?"
            url += parsed.query

    return url