from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from Extractor.Extractor.DatabaseLayer.db_consumer import DBConsumer
from Extractor.spiders.JobinjaExtractor import JobInjaExtractor
from Extractor.Processor.processor_consumer import RawDataConsumer

import multiprocessing


def run_consumer():
    """
    Function to start the data consumer process.
    """
    consumer = RawDataConsumer()
    consumer.run()


def run_spider():
    """
    Function to run the Scrapy spider
    """
    # Get settings
    settings = get_project_settings()

    # Initialize the crawler process
    process = CrawlerProcess(settings)

    # Add the spider to the process
    process.crawl(JobInjaExtractor)

    # Start the crawler
    process.start()


def run_db_consumer():
    """
    Function to start the db consumer process.
    """
    consumer = DBConsumer()
    consumer.run()


if __name__ == "__main__":
    # making the processes
    raw_consumer_process = multiprocessing.Process(target=run_consumer)
    db_consumer_process = multiprocessing.Process(target=run_db_consumer)
    spider_process = multiprocessing.Process(target=run_spider)

    # Start processes
    raw_consumer_process.start()
    spider_process.start()
    db_consumer_process.start()

    # Wait for both processes to complete
    spider_process.join()
    raw_consumer_process.join()
    db_consumer_process.join()
