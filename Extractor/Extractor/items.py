import scrapy


class JobInjaJobListItem(scrapy.Item):
    job_title = scrapy.Field()
    job_link = scrapy.Field()
    job_company_name = scrapy.Field()
    job_city = scrapy.Field()
    job_contract_type = scrapy.Field()

    company_image_url = scrapy.Field()
    company_category = scrapy.Field()
    company_population = scrapy.Field()
    company_website = scrapy.Field()
    job_minimum_work_experience = scrapy.Field()
    job_salary = scrapy.Field()
    job_content = scrapy.Field()
    company_biography = scrapy.Field()
