from typing import Any
from scrapy.http import Response
from scrapy.spiders import Spider
from ..items import JobInjaJobListItem


# the name of stuff
class JobInjaExtractor(Spider):
    name = "JobInjaExtractor"
    allowed_domains = ["jobinja.ir"]
    start_urls = [
        "https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85"
        "-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81"
        "%D8%B2%D8%A7%D8%B1"]

    def parse(self, response: Response, **kwargs: Any):
        all_job_adds = response.css("li.o-listView__item")
        for job_add in all_job_adds:
            job_list_item = JobInjaJobListItem()

            job_list_item['job_title'] = job_add.css("a.c-jobListView__titleLink::text").get().strip().replace("\n", "")

            job_url = job_add.css("a.c-jobListView__titleLink::attr(href)").get().strip()
            job_list_item['job_link'] = job_url

            job_list_item['job_company_name'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--construction + span::text").get().strip().replace("\n", "")

            job_list_item['job_city'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--place + span::text").get().strip().replace(
                "\n", "")

            job_list_item['job_contract_type'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--resume + span span::text").get().replace(" ", "").replace("\n",
                                                                                                                "")
            yield response.follow(job_url, callback=self.process_ad, cb_kwargs={'job_list_item': job_list_item})

        all_job_adds.clear()

        maximum_page_number = int(response.css("#js-jobSearchPaginator a::text").extract()[-2])
        page_number = 2
        next_page = (f"https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8"
                     f"%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9"
                     f"%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1?&page={str(page_number)}")
        print(f"-----------------------------{page_number}--{maximum_page_number}------------------------------------")
        if page_number <= maximum_page_number:
            print(f"--------------{next_page}")
            page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def process_ad(self, response: Response, job_list_item, **kwargs: Any):

        company_image_url = response.css(".c-companyHeader__logoImage::attr(src)").get()
        company_category = response.css(
            '.c-companyHeader__metaItem:nth-child(1) .c-companyHeader__metaLink').css("::text").get()
        company_population = response.css('.c-companyHeader__metaItem:nth-child(2)::text').get().strip().replace("\n",
                                                                                                                 "")
        company_website = response.css(
            ".c-companyHeader__metaItem+ .c-companyHeader__metaItem .c-companyHeader__metaLink").css("::text").get()
        job_minimum_work_experience = response.css(".c-jobView__firstInfoBox .c-infoBox__item:nth-child(4) .black").css(
            "::text").get()
        job_salary = response.css(".c-infoBox__item:nth-child(5) .black").css("::text").get().strip().replace("\n", "")
        job_content = response.css("div.s-jobDesc::text").get()
        company_biography = response.css(".c-pr40p~ .o-box__text").css("::text").get().strip().replace("\n", "")

        job_list_item["company_image_url"] = company_image_url
        job_list_item["company_category"] = company_category
        job_list_item["company_population"] = company_population
        job_list_item["company_website"] = company_website
        job_list_item["job_minimum_work_experience"] = job_minimum_work_experience
        job_list_item["job_salary"] = job_salary
        job_list_item["job_content"] = job_content
        job_list_item["company_biography"] = company_biography
        print(job_list_item["company_biography"])
        yield job_list_item
