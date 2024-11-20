from . import JobCreateDTO
from ..rediscodes.redislist import RedisList
from ..DatabaseLayer.db_code import save_job_to_database


class DBConsumer:
    def __init__(self):
        """
        Initializes the DBConsumer instance by setting up a RedisList object
        to listen to the 'processed_data' Redis channel.
        """
        self.redis = RedisList(channel='processed_data')

    @staticmethod
    def process_message(message):
        """
        Processes a single message by saving it to the database.

        Args:
            message (JobCreateDTO): The message object containing job data
                                    to be stored in the database.
        """
        save_job_to_database(message)

    def run(self):
        """
        Starts the consumer to continuously listen for messages from the Redis
        queue. Each message is processed as it is received.
        """
        while True:
            # Blocks until a message is received from the Redis queue
            raw_message: JobCreateDTO = self.redis.blocking_right_pop()
            # Process the retrieved message
            self.process_message(raw_message)
