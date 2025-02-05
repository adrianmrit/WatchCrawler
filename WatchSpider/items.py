import scrapy


class Watch(scrapy.Item):
    url = scrapy.Field()
    brand = scrapy.Field()

    reference = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    origin = scrapy.Field()
    collection = scrapy.Field()
    water_resistance = scrapy.Field()
    case_shape = scrapy.Field()
    case_diameter = scrapy.Field()
    case_width = scrapy.Field()
    case_length = scrapy.Field()
    case_thickness = scrapy.Field()
    case_back = scrapy.Field()
    crystal = scrapy.Field()
    case_material = scrapy.Field()
    weight = scrapy.Field()
    lugs_width = scrapy.Field()
    movement_type = scrapy.Field()
    caliber_diameter = scrapy.Field()
    movement_model = scrapy.Field()
    jewels = scrapy.Field()
    time = scrapy.Field()
    caliber = scrapy.Field()
    battery = scrapy.Field()
    functions = scrapy.Field()
    dial_color = scrapy.Field()
    indexes = scrapy.Field()
    strap_material = scrapy.Field()
    buckle = scrapy.Field()
    strap_color = scrapy.Field()
    features = scrapy.Field()