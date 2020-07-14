import unittest
import datetime
import decimal

import psycopg2
from freezegun import freeze_time

from monitor_consumer.models import MonitorEvent
from monitor_consumer.psql import PSQL

DB_CONNECT = {
    'host': 'localhost',
    'port': '5432',
    'user': 'monitor_event',
    'password': 'monitor_event',
    'database': 'monitor_event_test',
}

TABLE_NAME_EVENTS = 'system_monitor_events'


def drop_database():
    psql = PSQL(**DB_CONNECT)
    with psql.connection() as connect:
        with connect.cursor() as cursor:
            try:
                cursor.execute("TRUNCATE %s RESTART IDENTITY;" % TABLE_NAME_EVENTS)
            except psycopg2.errors.UndefinedTable:
                pass


class MonitorEventTest(unittest.TestCase):
    def setUp(self) -> None:
        drop_database()

    def test_monitor_event_add(self):
        now = datetime.datetime(2020, 7, 8, 22, 11, 33, 678240)
        psql = PSQL(**DB_CONNECT)
        with freeze_time(now):
            with psql.connection() as connection:
                repo = MonitorEvent(connection)
                repo.add("test", 200, 1.1, datetime.datetime.now(), False)

                cursor = repo.connect.cursor()
                cursor.execute("SELECT * FROM %s" % TABLE_NAME_EVENTS)
                records = cursor.fetchall()

                self.assertEqual(len(records), 1)
                self.assertEqual(records[0][0], 1)
                self.assertEqual(records[0][1], 'test')
                self.assertEqual(records[0][2], 200)
                self.assertEqual(records[0][3], decimal.Decimal('1.1'))
                self.assertEqual(records[0][4], False)
                self.assertEqual(records[0][5].replace(tzinfo=None), now)
