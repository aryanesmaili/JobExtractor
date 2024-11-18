import redis


class RedisQueue:
    def __init__(self, host='localhost', port=9090, channel='raw_data'):
        self.redis = redis.Redis(host=host, port=port, charset="utf-8", decode_responses=True)
        self.channel = channel

    def publish(self, message):
        """Publish a message to the Redis channel."""
        self.redis.publish(self.channel, message)

    def subscribe(self):
        """Subscribe to the Redis channel."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channel)
        return pubsub
