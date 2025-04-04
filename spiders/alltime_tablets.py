

import scrapy
from scrapy import Request

'''
    Создание Отдельного проекта Scrapy
    
    scrapy startproject alltime .
'''

'''
    Создание собственного спайдера

    scrapy genspider НАЗВАНИЕ  url
'''

'''
    Запуск спайдера
    
    scrapy crawl Название выше созданного спайдера
'''
class AlltimeTabletsSpider(scrapy.Spider):
    # Название Спайдера
    name = "alltime_tablets"
    allowed_domains = ["www.alltime.ru"]
    start_urls = ["https://www.alltime.ru/watch/"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1, # Ограничиваем количество одновременных запросов для предотвращения блокировки
        'DOWNLOAD_DELAY': 2, # Задержка между запросами для уменьшения нагрузки на сервер
    }


    def start_requests(self):
        self.current_page = 1
        urls = [f'https://www.alltime.ru/watch/?PAGEN_1={i}' for i in range(1, 10)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Прокладываем путь к нужным данным к html тегам
        products_items = response.css('a.catalog-item-link>span::text').extract()
        product_prices = response.css('div.catalog-item-price-prices > span.catalog-item-price.text-h5::text').extract()
        # Возврат результата
        print('---------------------------------------')
        print(products_items)
        print(product_prices)
        print(f'\n\n\n\nprocessig {response.url} status: {response.status}\n\n\n\n\n')
        print('---------------------------------------')
        row_data = zip(products_items, product_prices)
        for item in row_data:
            scared_info = {
                'page': response.url+f'?PAGEN_1={self.current_page}',
                'product_name': item[0],
                'price': item[1]
            }
            yield scared_info
            self.current_page += 1



