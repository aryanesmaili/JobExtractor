import redis


class RedisList:
    def __init__(self, host='localhost', port=9090, channel='raw_data'):
        self.redis = redis.Redis(host=host, port=port, charset="utf-8", decode_responses=True)
        self.channel = channel

    def left_push(self, message):
        """Publish a message to the Redis list."""
        self.redis.lpush(self.channel, message)

    def blocking_right_pop(self):
        """Pop an item from redis list"""
        _, raw_message = self.redis.brpop([self.channel],5)  # Blocks until a message is available
        return raw_message
