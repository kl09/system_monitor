import time
import logging
from datetime import datetime, timedelta

from kafka.errors import KafkaError
from monitor_producer.checker import WebChecker
from monitor_producer.producer import Producer
from monitor_producer.utils import Website

logger = logging.getLogger('monitor_producer')


class Runner:
    """
    Runner to periodical checking websites statuses.
    """

    def __init__(self, sites: [Website], producer: Producer, topic: str):
        """
        Creates a runner to check websites statuses.
        :param sites: list of websites to check
        :param producer: producer for sending results
        :param topic: Name of producer topic
        """

        self.websites: [Website] = sites
        self.backlog: map = {}
        self.producer: Producer = producer
        self.kafka_topic: str = topic

    def update_websites(self, sites: [Website]):
        """
        Update list of sites for checking in real time.

        :param sites: list of websites
        :return:
        """
        self.websites = sites

    def run(self, delay: int = 1):
        """
        Run loop for checking
        :param delay: delay in seconds between each iterations.
        :return:
        """
        logger.debug('start job loop')

        while True:
            self.check()
            time.sleep(delay)

    def check(self):
        """
        Run a single check by all websites.
        :return:
        """
        for website in self.websites:
            last_run = self.backlog.get(website.code)

            if not last_run or last_run + timedelta(seconds=website.check_interval) < datetime.now():
                try:
                    # TODO think about async checking
                    logger.debug('start checking url: %s with pattern: %s' % (website.url, website.regexp_pattern))
                    status_code, duration, found = WebChecker().check(website.url, website.regexp_pattern)

                    self.producer.send(
                        topic=self.kafka_topic,
                        msg={
                            'url': website.url,
                            'status_code': status_code,
                            'request_duration': duration,
                            'created_at': datetime.now(),
                            'found': found if website.regexp_pattern else ''
                        },
                    )

                except KafkaError as exc:
                    logger.error(
                        'Failed to push to kafka: %s, err: %s' % (website.url, exc),
                    )

                except Exception as exc:
                    logger.error(
                        'Failed to check url: %s, err: %s' % (website.url, exc),
                    )
                finally:
                    self.backlog[website.code] = datetime.now()
