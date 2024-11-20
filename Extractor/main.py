from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Extractor.spiders.JobinjaExtractor import JobInjaExtractor
from Extractor.Processor.Consumer import DataConsumer
import threading

def run_consumer():
    """
    Function to start the data consumer process.
    """
    consumer = DataConsumer()
    consumer.run()  # Assuming your Consumer class has a start() method for the queue

if __name__ == "__main__":
    # Get settings (optional if your project uses Scrapy settings)
    settings = get_project_settings()

    # Start the consumer in a separate thread
    consumer_thread = threading.Thread(target=run_consumer, daemon=True)
    consumer_thread.start()

    # Initialize the crawler process
    process = CrawlerProcess(settings)

    # Add the spider to the process
    process.crawl(JobInjaExtractor)

    # Start the crawler (blocking call)
    process.start()

    # Optionally join the consumer thread if needed
    consumer_thread.join()
