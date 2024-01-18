# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobInjaJobListItem(scrapy.Item):
    job_title = scrapy.Field()
    job_link = scrapy.Field()
    job_company_name = scrapy.Field()
    job_city = scrapy.Field()
    job_contract_type = scrapy.Field()