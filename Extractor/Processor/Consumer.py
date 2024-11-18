import json

from Extractor.redis.redisqueue import RedisQueue


class DataConsumer:
    def __init__(self, redis_host='localhost', redis_port=9090, channel='raw_data'):
        self.queue = RedisQueue(host=redis_host, port=redis_port, channel=channel)

    def process_message(self, message):
        """
        Custom logic to process the message.
        `message` is typically a JSON string representing raw data.
        """
        data = json.loads(message)  # Parse the JSON string back to a dictionary
        # Process the item here:

    def run(self):
        """
        Continuously listen to the Redis channel for new messages.
        """
        pubsub = self.queue.subscribe()
        print(f"Subscribed to channel: {self.queue.channel}")

        for message in pubsub.listen():
            if message['type'] == 'message':  # Ensure it's an actual message
                self.process_message(message['data'])
