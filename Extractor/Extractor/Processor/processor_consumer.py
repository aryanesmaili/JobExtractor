import json

from .OutputModel import JobDetails
from .ai_processor import ai_process
from ..DatabaseLayer import JobCreateDTO
from ..items import JobInjaJobListItem
from ..rediscodes.redislist import RedisList


class RawDataConsumer:
    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.raw_data_redis = RedisList(host=redis_host, port=redis_port, channel=channel)
        self.processed_data_redis = RedisList(host=redis_host, port=redis_port, channel='processed_data')

    @staticmethod
    def process_message(message):
        """
        Custom logic to process the message.
        `message` is typically a JSON string representing raw data.
        """
        data: JobInjaJobListItem = json.loads(message)  # Parse the JSON string back to a dictionary
        # Process the item here:
        processed_item: JobDetails = ai_process(data)
        result = JobCreateDTO(data, processed_item)
        return result

    def run(self):
        """
        Continuously listen to the Redis list and process messages.
        """
        while True:
            raw_message = self.raw_data_redis.blocking_right_pop()  # Block until a message is available
            result = self.process_message(raw_message)
            self.processed_data_redis.left_push(result)
