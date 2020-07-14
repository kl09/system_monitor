import logging

from kafka import KafkaConsumer

logger = logging.getLogger('monitor_consumer')


class Consumer:
    """
    Consumer gets messages from kafka.
    """

    def __init__(self, topic: str, **kwargs):
        """
        Creates a producer with params.
        :param topic: Name of topic
        :param kwargs:
        """
        self.consumer = KafkaConsumer(
            topic,
            **kwargs
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def get(self):
        """
        Get messages from kafka topic.
        :return:
        """
        for msg in self.consumer:
            yield msg

    def close(self):
        """
        Close connection to producer.
        :return:
        """
        self.consumer.close()
