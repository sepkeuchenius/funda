import scrapy
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response
import subprocess
import re
import scrapy
import logging

from time import sleep
class FundaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    price = scrapy.Field()              # Listing price ("Vraagprijs")
    year_built = scrapy.Field()         # Year built ("Bouwjaar")
    area = scrapy.Field()               # Built area ("Woonoppervlakte")
    rooms = scrapy.Field()              # Number of rooms
    bedrooms = scrapy.Field()           # Number of bedrooms
    property_type = scrapy.Field()      # House or apartment
    city = scrapy.Field()
    posting_date = scrapy.Field()
    sale_date = scrapy.Field()
class FundaSoldSimpleSpider(Spider):

    name = "funda_sold_simple"
    allowed_domains = ["funda.nl"]

    def __init__(self, place='utrecht'):
        url = f"https://www.funda.nl/koop/{place}/"
        self.start_urls = [url]
        self.base_url = url
        self.le1 = LinkExtractor(allow=r'%s+(huis|appartement)-\d{8}' % self.base_url)
        logging.warning(self.le1)
        custom_settings = {
            "COOKIES_ENABLED": False,
            "DOWNLOAD_DELAY": 5,
            "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        logging.warning(custom_settings)
        self.custom_settings = custom_settings
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
    
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        logging.warning("Setting user agent")
        settings.set("USER_AGENT","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", priority="spider")

    def parse(self, response:Response):
        links = self.le1.extract_links(response)
        logging.warning(links)
        for link in links:
            if link.url.endswith('/'):
                item = FundaItem()
                item['url'] = link.url
                logging.warning(item)

                if re.search(r'/appartement-',link.url):
                    item['property_type'] = "apartment"
                elif re.search(r'/huis-',link.url):
                    item['property_type'] = "house"
                yield scrapy.Request(link.url, callback=self.parse_dir_contents, meta={'item': item})

    def parse_dir_contents(self, response:Response):
        new_item = response.request.meta['item']
        title = response.xpath('//title/text()').extract()[0]
        postal_code = re.search(r'\d{4} [A-Z]{2}', title).group(0)
        city = re.search(r'\d{4} [A-Z]{2} \w+',title).group(0).split()[2]
        address = re.findall(r'te koop: (.*) \d{4}',title)[0]
        price_dd = response.xpath("//dt[contains(.,'Vraagprijs')]/following-sibling::dd[1]/span/text()").extract()[0]
        price = re.findall(r' \d+.\d+', price_dd)[0].strip().replace('.','')
        year_built_dd = response.xpath("//dt[contains(.,'Bouwjaar')]/following-sibling::dd[1]/span/text()").extract()[0]
        year_built = re.findall(r'\d+', year_built_dd)[0]
        area_dd = response.xpath("//dt[contains(.,'Wonen')]/following-sibling::dd[1]/span/text()").extract()[0]
        area = re.findall(r'\d+', area_dd)[0]
        rooms_dd = response.xpath("//dt[contains(.,'Aantal kamers')]/following-sibling::dd[1]/span/text()").extract()[0]
        rooms = re.findall('\d+ kamer',rooms_dd)[0].replace(' kamer','')
        bedrooms = re.findall('\d+ slaapkamer',rooms_dd)[0].replace(' slaapkamer','')

        new_item['postal_code'] = postal_code
        new_item['address'] = address
        new_item['price'] = price
        new_item['year_built'] = year_built
        new_item['area'] = area
        new_item['rooms'] = rooms
        new_item['bedrooms'] = bedrooms
        new_item['city'] = city
        yield new_item


def search()->dict:
    import json
    path = 'out/results.json'
    subprocess.run(['scrapy', 'runspider', 'src/utils/funda.py', f'-o {path}'])
    with open(path) as file:
        return json.load(file)