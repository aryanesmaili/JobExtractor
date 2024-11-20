import redis


class RedisList:
    """
    A wrapper around Redis to interact with a Redis list, providing methods
    to push and pop messages from a Redis channel.

    Attributes:
        host (str): The Redis server hostname. Defaults to 'localhost'.
        port (int): The Redis server port. Defaults to 9090.
        channel (str): The Redis list (channel) name. Defaults to 'raw_data'.
    """
    def __init__(self, host='localhost', port=9090, channel='raw_data'):
        """
        Initializes a RedisList instance with the specified Redis server
        and channel.

        Args:
            host (str): The Redis server hostname. Defaults to 'localhost'.
            port (int): The Redis server port. Defaults to 9090.
            channel (str): The Redis list (channel) name. Defaults to 'raw_data'.
        """
        self.redis = redis.Redis(
            host=host,
            port=port,
            charset="utf-8",
            decode_responses=True
        )  # Configures Redis client with UTF-8 encoding
        self.channel = channel

    def left_push(self, message):
        """
        Publishes (pushes) a message to the Redis list on the left side.

        Args:
            message (str): The message to push onto the Redis list.
        """
        self.redis.lpush(self.channel, message)

    def blocking_right_pop(self):
        """
        Blocks until a message is available on the right side of the Redis list
        and pops it. Returns the message.

        Returns:
            str: The message popped from the Redis list.

        Raises:
            TimeoutError: If no message is received within 5 seconds.
        """
        # Pop a message from the right side of the Redis list, blocking for up to 5 seconds
        result = self.redis.brpop([self.channel], 5)
        if result is None:
            raise TimeoutError("No message received from the Redis list within the timeout period.")
        _, raw_message = result
        return raw_message
