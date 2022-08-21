from json import loads

from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess


class RozetkaScraper(Spider):
    name = 'rozetka'

    def start_requests(self):
        yield Request('https://msd-rk.rozetka.com.ua/rk/search?text=мужские%20кроссовки', callback=self.search_products)
    
    def parse_pages(self, response):
        yield Request('https://search.rozetka.com.ua/search/api/v6/?front-type=xl&country=UA&lang=ru&section_id=4634865&page=29&text=%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B8%D0%B5+%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BE%D0%B2%D0%BA%D0%B8', callback=self.parse_ids)

    def parse_ids(self, response):
        product_ids = loads(response.text)
        product_param = ','.join([str(product['id']) for product in product_ids])
        yield Request(f'https://xl-catalog-api.rozetka.com.ua/v4/goods/getDetails?product_ids={product_param}', callback=self.parse_products)

    def parse_products(self, response):
        product_data = loads(response.text)['data']
        
        for product in product_data:
            yield {
                'title': product['title'],
                'price': product['price'],
                'status': product['status'],
                'image': product['image_main'],
                'stars': product['stars'],
                'comments': product['comments_amount'],
            }


process = CrawlerProcess()
process.crawl(RozetkaScraper)
process.start()
