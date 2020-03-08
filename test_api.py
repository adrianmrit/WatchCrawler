import requests
import json
from PIL import Image
from io import BytesIO
import json
import argparse

config = json.load(open('config.json'))

# watch = {
#     "brand": "Wenger",
#     "price": "$1,307.98",
#     "url": None,
#     "gender": "Mens",
#     "reference": "L3.781.4.76.9",
#     "image": "https://www.worldofwatches.com/media/catalog/product/cache/cd4ffe7bf38b59f96d8178d3c42277fa/m/e/mens-hydroconquest-rubber-grey-dial-l37814769.jpg",
#     "name": "Men's Hydroconquest Rubber Grey Dial",
#     "description": None,
#     "origin": None,
#     "collection": "HydroConquest",
#     "water_resistance": "300 meters / 1000 feet",
#     "case_shape": "Round",
#     "bezel_material": "Ceramic",
#     "case_diameter": "41 mm",
#     "case_width": None,
#     "case_length": None,
#     "case_thickness": None,
#     "case_back": None,
#     "crystal": "Scratch Resistant Sapphire",
#     "case_material": "Stainless Steel",
#     "weight": None,
#     "lugs_width": None,
#     "movement_type": "Automatic",
#     "caliber_diameter": None,
#     "movement_model": "Longines Calibre L619/888",
#     "jewels": None,
#     "time": "Date, Hour, Minute, Second",
#     "caliber": None,
#     "battery": None,
#     "functions": "Date, Hour, Minute, Second",
#     "dial_color": "Grey",
#     "indexes": None,
#     "strap_material": None,
#     "buckle": None,
#     "strap_color": None,
#     "features": "Calendar, Ceramic, Rubber, Stainless Steel",
#     "store": "WorldOfWatches",
#     "sale_url": "https://www.worldofwatches.com/mens-hydroconquest-rubber-grey-dial-longines-l3-781-4-76-9-lng37814769",
#     "currency": "USD"
# }
image = requests.get("https://cdn.shopify.com/s/files/1/1786/0047/products/1M-SP74B7G-straight_400x.jpg?v=1580779762")

def test(watch):
    img = Image.open(BytesIO(image.content))

    byte_io = BytesIO()
    img.save(byte_io, 'JPEG')  # convert the image to JPEG and save it as bytestring

    files = {'image': (watch['reference']+watch['name']+".jpg", byte_io.getvalue(), "image/jpeg")}

    response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})
    print(response.status_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test using a json file for a watch')
    parser.add_argument('--file', metavar='path', required=True,
                        help='the path to the json file')
    args = parser.parse_args()
    test(json.load(open(args.file)))