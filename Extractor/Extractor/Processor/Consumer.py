import json
import time

from ..DatabaseLayer import JobCreateDTO
from ..DatabaseLayer.dbfuncs import save_to_database
from ..items import JobInjaJobListItem
from ..rediscodes.redislist import RedisList
from .OutputModel import JobDetails
from .ai_processor import ai_process


class DataConsumer:
    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.redis = RedisList(host=redis_host, port=redis_port, channel=channel)
        self.running = True
        self.channel = channel

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
        save_to_database(result)

    def run(self):
        """
        Continuously listen to the Redis list and process messages.
        """
        print(f"Listening to list: {self.channel}")
        while True:
            raw_message = self.redis.blocking_right_pop()  # Block until a message is available
            self.process_message(raw_message)
            time.sleep(3)