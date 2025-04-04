from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from alltime.spiders.chokolat import ChokolatSpider


class DataCollector:
    def __init__(self):
        self.items = []

    def collect_item(self, item):
        self.items.append(item)
        return item


# Создаем сборщик данных
data_collector = DataCollector()

# Модифицируем паука на лету
original_parse = ChokolatSpider.parse


def modified_parse(self, response):
    for item in original_parse(self, response):
        data_collector.collect_item(item)
        yield item


ChokolatSpider.parse = modified_parse

# Настройки (минимальные)
settings = {
    'USER_AGENT': 'Mozilla/5.0',
    'ROBOTSTXT_OBEY': True,
    'LOG_ENABLED': False
}

# Запускаем процесс
process = CrawlerProcess(settings)
process.crawl(ChokolatSpider)
process.start()

data = data_collector.items
print(data)
# Выводим результаты
print(f"\nСпарсено {len(data_collector.items)} товаров:")
for item in data_collector.items:
    print(f"{item['product']} - {item['price']}")
    print(f"Ссылка: {item['link']}\n")