from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import GplayItem



class GplaySpider(CrawlSpider):
    name = 'gplay'
    start_urls = ['https://gplay.bg']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='vue']/div[2]/div/div/div[2]/ul/li[1]/a",
                                            "//*[@id='vue']/div[2]/div/div/div[2]/ul/li[2]/a")),
             callback='parse_category',
             follow=True),
    )



    def parse_category(self, response):
        categories = response.xpath("//*[@id='content']/div[2]/div[2]/div[@class='categories-grid-item']")

        for category in categories:
            link = category.xpath(".//a/@href").get()

            yield response.follow(url=link, callback=self.parse_item_page)



    def parse_item_page(self, response):
        categories = response.xpath("//*[@id='desktop-form']/div/div[2]/div[5]/div[1]/div")
        subcategory = response.xpath("//*[@id='desktop-form']/div/div[2]/h1/text()").get()
        next_page = response.xpath("//*[@id='desktop-form']/div/div[2]/div[5]/div[2]/div/ul/li[last()]/a/@href").get()
        main_category = response.xpath("//*[@id='desktop-form']/div/div[2]/div[1]/a[2]/text()").get()

        for category in categories:
            link = category.xpath(".//div/a/@href").get()


            yield response.follow(url=link, callback=self.parse_item, meta={"next_page": next_page,
                                                                            "subcategory": subcategory,
                                                                            "main_category": main_category
                                                                            })



    def parse_item(self, response):
        items = GplayItem()
        products = response.xpath("//*[@id='content']/div[1]/div[2]/div[2]")

        for product in products:
            next_page = response.request.meta["next_page"]
            subcategory = response.request.meta["subcategory"]
            main_category = response.request.meta["main_category"].split(" ")[1]

            title = product.xpath(".//h1/text()").get()
            title_clean = title.replace("\n", "").strip()
            product_serial = product.xpath(".//div[1]/div[1]/strong/text()").get()
            product_subtitle = product.xpath(".//h2//text()").get()
            product_subtitle_clean = product_subtitle.replace("\n", "").strip()
            product_price = product.xpath(".//div[2]/div[1]/div").get()
            product_price_clean = float(product_price.split('=')[2].lstrip().split(">")[0].replace('"', ""))
            product_status = product.xpath(".//div[2]/span[1]/@title").get()

            if product_price_clean < 200 and product_status != "не е в наличност":
                items["category"] = main_category
                items["subcategory"] = subcategory
                items["title"] = title_clean
                items["subtitle"] = product_subtitle_clean
                items["product_number"] = product_serial
                items["price"] = product_price_clean

                yield items

            if next_page:
                yield response.follow(url=next_page, callback=self.parse_item_page)
