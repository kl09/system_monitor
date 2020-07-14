import json
import logging
from datetime import datetime, date

from kafka import KafkaProducer

logger = logging.getLogger('monitor_producer')


class Producer:
    """
    Kafka producer to produce messages.
    """

    def __init__(self, **kwargs):
        """
        Creates a producer with params.
        :param kwargs:
        """
        self.producer = KafkaProducer(
            **kwargs
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def send(self, topic: str, msg: dict):
        """
        Send a message to producer.
        :param topic: topic name
        :param msg: message to send
        :return:
        """
        data = json.dumps(msg, default=self._json_dumps_handler)

        logger.debug('Start writing msg to kafka topic: %s , data: %s' % (topic, data))
        self.producer.send(
            topic=topic,
            value=data.encode('utf-8'),
        )

    def _json_dumps_handler(self, obj):
        """
        Custom json encoder.
        :param obj:
        :return:
        """
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.ctime()
        return None

    def close(self):
        """
        Close connection to producer.
        :return:
        """
        self.producer.close()
