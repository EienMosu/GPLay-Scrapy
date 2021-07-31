import scrapy


class GplayItem(scrapy.Item):
    category = scrapy.Field()
    subcategory = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    product_number = scrapy.Field()
    price = scrapy.Field()
