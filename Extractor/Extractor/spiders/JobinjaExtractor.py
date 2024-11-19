from typing import Any

from scrapy.http import Response
from scrapy.spiders import Spider

from ..items import JobInjaJobListItem


# the name of stuff
class JobInjaExtractor(Spider):
    name = "JobInjaExtractor"
    allowed_domains = ["jobinja.ir"]
    start_urls = [
        "https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1"]
    page_number = 2

    def parse(self, response: Response, **kwargs: Any):
        """
        this function will first add all the advertises listed in the current page in the variable called 'all_job_adds'
        and then loops through the list of advertises and scrapes what we want from the list of advertises. then it will
        go through each of the advertises and then scrap the rest of the data that we want from within the advertises.
        :param response: the response received from Jobinja containing the HTML page and status code
        :param kwargs: nothing
        :returns: yields the item object containing an advertisement and all it's wanted data.
        """
        # storing the list of advertises in the variable
        all_job_adds = response.css("li.o-listView__item")

        for job_add in all_job_adds:
            # Creating a new Item Instance
            job_list_item = JobInjaJobListItem()

            # Scraping the values from the elements
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
            # Going Through the detailed page of job description using this function called response.follow and running
            # our scraping on it.
            yield response.follow(job_url, callback=self.process_ad, cb_kwargs={'job_list_item': job_list_item})

        # we clear the list of job advertisements when we've processed all of them.
        all_job_adds.clear()

        maximum_page_number = int(response.css("#js-jobSearchPaginator a::text").extract()[-2])
        next_page = (f"https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8"
                     f"%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9"
                     f"%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1?&page={str(JobInjaExtractor.page_number)}")
        if JobInjaExtractor.page_number <= maximum_page_number:
            yield response.follow(next_page, callback=self.parse)
            JobInjaExtractor.page_number += 1

    @staticmethod
    def process_ad(response: Response, job_list_item):
        """
        this function is called when we want to scrape the job advertisement in more detail.
        :param response: the page containing the job advertisement in more detailed manner.
        :param job_list_item: the job advertisement item for this job advertisement.
        :return: yields the completed job advertisement scraped item.
        """
        job_list_item["company_image_url"] = response.css(".c-companyHeader__logoImage::attr(src)").get()

        job_list_item["company_category"] = (
            response.css('.c-companyHeader__metaItem:nth-child(1) .c-companyHeader__metaLink')
            .css("::text").get())

        job_list_item["company_population"] = response.css(
            '.c-companyHeader__metaItem:nth-child(2)::text').get().strip().replace("\n", "")

        job_list_item["company_website"] = response.css(
            ".c-companyHeader__metaItem+ .c-companyHeader__metaItem .c-companyHeader__metaLink").css("::text").get()

        job_list_item["job_minimum_work_experience"] = response.css(
            ".c-jobView__firstInfoBox .c-infoBox__item:nth-child(4) .black").css("::text").get()

        job_list_item["job_salary"] = (response.css(".c-infoBox__item:nth-child(5) .black").css("::text").get().strip()
                                       .replace("\n", ""))

        job_content = response.css('div.o-box__text.s-jobDesc ::text').getall()

        job_list_item["job_content"] = ' '.join([x.strip() for x in job_content])

        job_list_item["national_service_status"] = response.css(".u-mB0 .c-infoBox__item:nth-child(3) .black").css(
            "::text").get()

        yield job_list_item
