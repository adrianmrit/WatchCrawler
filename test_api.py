import requests
import json
from PIL import Image
from io import BytesIO
import json
import argparse
from scrapy.utils.project import get_project_settings
from utils.images import load_img_from_request

PROJECT_SETTINGS = get_project_settings()

HEADERS = {'User-Agent': get_project_settings()['USER_AGENT']}  # headers to use with non scrapy requests
config = json.load(open('config.json'))




def test(watch):
    image = requests.get(watch['image'], headers=HEADERS)
    image = load_img_from_request(image)

    files = {'image': (watch['reference']+watch['name']+".jpg", image, "image/jpeg")}

    response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})
    print(response.status_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test using a json file for a watch')
    parser.add_argument('--file', metavar='path', required=True,
                        help='the path to the json file')
    args = parser.parse_args()
    test(json.load(open(args.file)))