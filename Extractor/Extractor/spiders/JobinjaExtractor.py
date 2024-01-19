from typing import Any
from scrapy.http import Response
from scrapy.spiders import Spider
from ..items import JobInjaJobListItem


# the name of stuff
class JobInjaExtractor(Spider):
    name = "JobInjaExtractor"
    start_urls = [
        "https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1"]

    def parse(self, response: Response, **kwargs: Any):
        all_job_adds = response.css("li.o-listView__item")
        job_list_item = JobInjaJobListItem()

        for job_add in all_job_adds:
            job_list_item['job_title'] = job_add.css("a.c-jobListView__titleLink::text").get().strip().replace("\n", "")

            job_list_item['job_link'] = job_add.css("a.c-jobListView__titleLink::attr(href)").get().strip()

            job_list_item['job_company_name'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--construction + span::text").get().strip().replace("\n", "")

            job_list_item['job_city'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--place + span::text").get().strip().replace(
                "\n", "")

            job_list_item['job_contract_type'] = job_add.css(
                "li.c-jobListView__metaItem i.c-icon--resume + span span::text").get().replace(" ", "").replace("\n",
                                                                                                                "")
            yield job_list_item

        job_list_item.clear()

    def process_ad(self, response: Response, **kwargs: Any):
        pass
