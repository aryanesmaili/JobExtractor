from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Extractor.spiders.JobinjaExtractor import JobInjaExtractor
from Extractor.Processor.Consumer import DataConsumer
import multiprocessing

def run_consumer():
    """
    Function to start the data consumer process.
    """
    consumer = DataConsumer()
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

if __name__ == "__main__":
    # Use multiprocessing instead of threading
    consumer_process = multiprocessing.Process(target=run_consumer)
    spider_process = multiprocessing.Process(target=run_spider)

    # Start both processes
    consumer_process.start()
    spider_process.start()

    # Wait for both processes to complete
    spider_process.join()
    consumer_process.join()