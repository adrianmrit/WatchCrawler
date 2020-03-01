import json

data = {
    'brand': '',
    'allowed_domains': [],
    'start_urls' : [],
    'allowed_watches_urls': [],
    'allowed_collections_urls': [],
    "default_origin": "",
    'xpaths': {
        'reference': '',
        'name': '',
        "description": "",
        'origin': '',
        'collection': '',

        'water_resistance': '',

        'case_shape': '',
        'case_width': '',
        'case_length': '',
        'case_thickness': '',
        'case_back': '',
        'crystal': '',
        'case_material': '',

        'weight': '',
        'lugs_width': '',

        'movement_type': '',
        'caliber_diameter': '',
        'movement_model': '',
        'jewels': '',
        'time': '',
        'caliber': '',
        'battery': '',

        'functions': '',

        'dial_color': '',
        'indexes': '',
        'strap_material': '',
        'buckle': '',
        'strap_color': '',
        'features': '',
    }
}

with open('base.json', 'w') as fp:
    json.dump(data, fp, indent=4)