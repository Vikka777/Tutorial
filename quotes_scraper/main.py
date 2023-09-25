import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

#Ці класи визначають структуру даних для зберігання
class QuoteItem(Item):
    keywords = Field()
    author = Field()
    quote = Field()

class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()

#Використовується для обробки даних після їхнього збору з веб-сторінки 
class QuotesPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if isinstance(item, QuoteItem):
            self.quotes.append({
                "tags": adapter["keywords"],
                "author": adapter["author"],
                "quote": adapter["quote"],
            })

        if isinstance(item, AuthorItem):
            self.authors.append({
                "fullname": adapter["fullname"],
                "born_date": adapter["born_date"],
                "born_location": adapter["born_location"],
                "description": adapter["description"],
            })

        return item

#Викликається при завершенні роботи павука та виконує запис даних у JSON файли.
    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=4)

        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=4)

#Парсинг даних (цитат) з веб-сторінки
class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        "ITEM_PIPELINES": {QuotesPipline: 300},
        "FEED_FORMAT": "json",  # This sets the output format to JSON
        "FEED_URI": "quotes.json"  # This specifies the output file for quotes
    }
##Парсинг даних (авторів) з веб-сторінки
    def parse(self, response, *args):
        for quote in response.xpath("/html//div[@class='quote']"):
            keywords = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(keywords=keywords, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.nested_parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response, *args):
        author = response.xpath('/html//div[@class="author-details"]')
        fullname = author.xpath('h3[@class="author-title"]/text()').get().strip()
        date_born = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        location_born = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        bio = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=date_born, born_location=location_born, description=bio)

if __name__ == '__main__':
    process = CrawlerProcess() #створення об'єкту
    process.crawl(QuotesSpider) #запуск парсингу
    process.start()
