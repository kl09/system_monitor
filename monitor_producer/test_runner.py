import unittest
import datetime
from unittest import mock

from freezegun import freeze_time

from monitor_producer.runner import Runner
from monitor_producer.utils import Website
from monitor_producer.producer import Producer

websites = [
    Website('localhost', 1, '', ),
    Website('localhost', 3, ''),
    Website('localhost', 4, 'some text'),
]

KAFKA_SETTINGS = {
    'bootstrap_servers': ['localhost:9093'],
    'acks': 'all',
    'security_protocol': 'SASL_PLAINTEXT',
    'sasl_mechanism': 'SCRAM-SHA-512',
    'sasl_plain_username': 'adminuser',
    'sasl_plain_password': 'admin-secret-512',
}

KAFKA_TOPIC = 'website_checks'


class RunnerTest(unittest.TestCase):
    @mock.patch('requests.get')
    def test_backlog_check(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        with Producer(**KAFKA_SETTINGS) as producer:
            runner = Runner(websites, producer, KAFKA_TOPIC)
            runner.check()

        self.assertEqual(len(runner.backlog), 3)
        self.assertEqual(requests_get.call_count, 3)

    @mock.patch('requests.get')
    def test_backlog_check_double_time(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        with Producer(**KAFKA_SETTINGS) as producer:
            runner = Runner(websites, producer, KAFKA_TOPIC)
            runner.check()

        self.assertEqual(len(runner.backlog), 3)
        self.assertEqual(requests_get.call_count, 3)

    @mock.patch('requests.get')
    def test_backlog_check_double_time_with_pause(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        with Producer(**KAFKA_SETTINGS) as producer:
            runner = Runner(websites, producer, KAFKA_TOPIC)
            runner.check()
            self.assertEqual(requests_get.call_count, 3)
            self.assertEqual(len(runner.backlog), 3)

            with freeze_time(datetime.datetime.now() + datetime.timedelta(seconds=1)):
                runner.check()
                self.assertEqual(requests_get.call_count, 4)

            with freeze_time(datetime.datetime.now() + datetime.timedelta(seconds=2)):
                runner.check()
                self.assertEqual(requests_get.call_count, 5)

            with freeze_time(datetime.datetime.now() + datetime.timedelta(seconds=3)):
                runner.check()
                self.assertEqual(requests_get.call_count, 7)

    @mock.patch('requests.get')
    @mock.patch('monitor_producer.producer.Producer.send')
    def test_kafka_producer_msg_format(self, producer_send, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        now = datetime.datetime(2020, 7, 8, 22, 11, 33, 678240)
        with freeze_time(now):
            runner = Runner(websites, Producer(), KAFKA_TOPIC)
            runner.check()

            self.assertEqual(len(runner.backlog), 3)
            self.assertEqual(producer_send.call_count, 3)

            expected = [
                mock.call(
                    msg={
                        'url': 'localhost',
                        'status_code': 200,
                        'request_duration': 2.0001,
                        'created_at': now,
                        'found': '',
                    },
                    topic=KAFKA_TOPIC,
                ),
                mock.call(
                    msg={
                        'url': 'localhost',
                        'status_code': 200,
                        'request_duration': 2.0001,
                        'created_at': now,
                        'found': '',
                    },
                    topic=KAFKA_TOPIC,
                ), mock.call(
                    msg={
                        'url': 'localhost',
                        'status_code': 200,
                        'request_duration': 2.0001,
                        'created_at': now,
                        'found': True,
                    },
                    topic=KAFKA_TOPIC,
                ),
            ]

            self.assertEqual(producer_send.call_args_list, expected)
