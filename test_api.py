import requests
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

response = requests.post(config['server'], json=watch, headers={'Authorization':config['auth_token']})
print(response.status_code)