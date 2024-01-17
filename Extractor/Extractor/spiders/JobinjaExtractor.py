from typing import Any
from scrapy.http import Response
from scrapy.spiders import Spider


# the name of stuff
class JobInjaExtractor(Spider):
    name = "JobInjaExtractor"
    start_urls = ["https://www.jobinja.com/jobs/"]

    def parse(self, response: Response, **kwargs: Any):
        quote: list = response.css(".quote").extract()
        yield {"quote": quote}
