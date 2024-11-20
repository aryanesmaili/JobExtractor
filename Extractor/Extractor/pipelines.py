import json

from .items import JobInjaJobListItem
from .rediscodes.redislist import RedisList


class ExtractorPipeline:
    """Class to process extracted items and publish them to Redis."""

    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.redis_list = RedisList(host=redis_host, port=redis_port, channel=channel)

    def process_item(self, item : JobInjaJobListItem, spider):
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
            message = json.dumps(dict(item), ensure_ascii=False)
            self.redis_list.left_push(message)
            spider.logger.info(f"Published item to Redis: {message}")
            return item
        else:
            from scrapy.exceptions import DropItem
            raise DropItem("Missing item data")
