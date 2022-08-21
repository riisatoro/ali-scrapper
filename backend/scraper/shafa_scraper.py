from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess


class ShafaSpider(Spider):
    name = 'shafa'

    def start_requests(self):
        yield Request(f'https://shafa.ua/uk/clothes?search_text={self.search_text}')
    
    def parse(self, response):
        products_list = response.xpath('//ul[contains(@class, \'b-catalog\')]')
        for product in products_list.xpath('//li//div//a'):                
            url = product.xpath('@href').get()
            yield Request(f'https://shafa.ua{url}', callback=self.parse_product)

    def parse_product(self, response):
        product_title = response.xpath('//*[contains(@class, \'b-product__title\')]/text()').get()
        product_brand = response.xpath('//*[contains(@class, \'b-product-brand__title\')]/text()').get() or ''

        yield {
            'title': f'{product_title} {product_brand}',
            'price': response.xpath('//span[contains(@class, \'b-product-price__current\')]/span/text()').get(),
            'image': response.xpath('//img[contains(@class, \'b-product-gallery__image\')]/@src').get(),
            'url': response.url,
        }
