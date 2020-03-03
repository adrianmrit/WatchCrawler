import requests
import json
from PIL import Image
from io import BytesIO
import json

config = json.load(open('config.json'))

watch = {
    "url": "https://www.momentumwatch.com/collections/mens-watches/products/torpedo-pro-44mm",
    "brand": "Momentum",
    "reference": "1M-DV44BS0",
    "name": "Torpedo Pro [44mm]",
    "description": "Nobody counts on their watch more than a diver does. When you hit the water or the water hits you, you can count on the Torpedo like no other. Engineered for reliability, at a price that won\u2019t leave you gasping for air. The Torpedo Family includes the Torpedo Black-ion, Torpedo Blast, Torpedo Ion-Blast, Torpedo Pro 44mm & Torpedo Pro 29mm",
    "origin": None,
    "collection": None,
    "water_resistance": "200m / 660ft",
    "case_shape": None,
    "case_diameter": "44mm",
    "case_width": None,
    "case_length": None,
    "case_thickness": "12mm",
    "case_back": None,
    "crystal": "Sapphire / Mineral",
    "case_material": None,
    "weight": None,
    "lugs_width": "22mm",
    "movement_type": None,
    "caliber_diameter": None,
    "movement_model": "Japanese, Seiko VX32G",
    "jewels": None,
    "time": None,
    "caliber": None,
    "battery": "371",
    "functions": None,
    "dial_color": None,
    "indexes": None,
    "strap_material": None,
    "buckle": None,
    "strap_color": None,
    "features": None
}
image = requests.get("https://cdn.shopify.com/s/files/1/1786/0047/products/1M-SP74B7G-straight_400x.jpg?v=1580779762")
img = Image.open(BytesIO(image.content))
# img.save('image.jpg', 'JPEG')
byte_io = BytesIO()
img.save(byte_io, 'JPEG')
files = {'image': (watch['reference']+watch['name']+".jpg", byte_io.getvalue(), "image/jpeg")}
response = requests.post(config['server'], data={'json': json.dumps(watch)}, files=files, headers={'Authorization':config['auth_token']})
print(response.status_code)