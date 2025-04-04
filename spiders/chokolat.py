from typing import Iterable

import scrapy
from scrapy import Request


class ChokolatSpider(scrapy.Spider):
    name = "chokolat"
    allowed_domains = ["www.chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/all"]
    def start_requests(self):
        self.current_page = 1
        urls = [f'https://www.chocolate.co.uk/collections/all?page={i}' for i in range(1, 3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Название продукта
        name_product = response.css('div.product-item__info > div > a::text').extract()
        # Цена продукта
        price_product = response.css('div.product-item__info > div > div > div >span::text').extract()
        # Ссылка на продукт
        link_product = response.css('div.product-item__info > div > a::attr(href)').extract()
        # Фотография продукта
        img_product = response.css('div.product-item__image-wrapper > a > img::attr(src)').extract()
        data = zip(name_product, price_product, link_product,img_product)

        # print('-----------------------------')
        # print(name_product)
        # print(price_product)
        # print(link_product)
        # print(img_product)
        # print('-----------------------------')
        for elem in data:
            dct_result = {
                'product': elem[0].strip(),
                'price': elem[1].strip(),
                'link': 'https://www.chocolate.co.uk'+elem[2].strip(),
                'img': elem[3].strip().replace('//', '')
            }
            if not dct_result['price']:
                continue

            self.current_page += 1

            yield dct_result



# data = zip([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4])
#
# print(*data)