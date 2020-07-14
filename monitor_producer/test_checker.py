import unittest
import datetime
from unittest import mock

from monitor_producer.checker import WebChecker


class WebCheckerTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_success_parse_url(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        status_code, duration, found = WebChecker().check('')

        self.assertEqual(status_code, 200)
        self.assertEqual(duration, 2.0001)
        self.assertEqual(found, False)

    @mock.patch('requests.get')
    def test_success_parse_url_and_regexep_found(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        status_code, duration, found = WebChecker().check('', 'some text')

        self.assertEqual(status_code, 200)
        self.assertEqual(duration, 2.0001)
        self.assertEqual(found, True)

    @mock.patch('requests.get')
    def test_success_parse_url_and_regexep_not_found(self, requests_get):
        resp = mock.MagicMock()
        requests_get.return_value = resp
        resp.status_code = 200
        resp.content = '<html>some1 text</html>'
        resp.elapsed = datetime.timedelta(seconds=2.0, microseconds=100)

        status_code, duration, found = WebChecker().check('', 'some text')

        self.assertEqual(status_code, 200)
        self.assertEqual(duration, 2.0001)
        self.assertEqual(found, False)
