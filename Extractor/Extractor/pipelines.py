import json

from ..redis.redisqueue import RedisQueue


class ExtractorPipeline:
    """Class to process extracted items and publish them to Redis."""

    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.queue = RedisQueue(host=redis_host, port=redis_port, channel=channel)

    def process_item(self, item, spider):
        """
        Process an extracted item and publish it to Redis.

        Args:
            item: The extracted item.
            spider: The spider that extracted the item.

        Returns:
            item: The processed item.
        """

        if item:
            # Convert the item to JSON and publish it to Redis
            message = json.dumps(dict(item))
            self.queue.publish(message)
            spider.logger.info(f"Published item to Redis: {message}")
            return item
        else:
            from scrapy.exceptions import DropItem
            raise DropItem("Missing item data")
