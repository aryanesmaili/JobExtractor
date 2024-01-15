from typing import Any
from scrapy.http import Response
from scrapy.spiders import Spider


class JobInjaExtractor(Spider):
    name = "JobInjaExtractor"
    start_urls = ["https://www.jobinja.com/jobs/"]

    def parse(self, response: Response, **kwargs: Any):
        title: list = response.css("").extract()
        yield {"title": title}
