import json

from Extractor.Extractor.redis.redisqueue import RedisQueue
from OutputModel import JobDetails
from ai_processor import ai_process
from ..Extractor.DatabaseLayer.JobCreateDTO import JobCreateDTO
from ..Extractor.DatabaseLayer.dbfuncs import save_to_database
from ..Extractor.items import JobInjaJobListItem


class DataConsumer:
    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.queue = RedisQueue(host=redis_host, port=redis_port, channel=channel)

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
        Continuously listen to the Redis channel for new messages.
        """
        pubsub = self.queue.subscribe()
        print(f"Subscribed to channel: {self.queue.channel}")

        for message in pubsub.listen():
            if message['type'] == 'message':  # Ensure it's an actual message
                self.process_message()
