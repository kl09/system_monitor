import logging
import json

from monitor_consumer.consumer import Consumer
from monitor_consumer.models import MonitorEvent
from monitor_consumer.psql import PSQL
from monitor_consumer.utils import LogHandler, parse_json_settings

logger = logging.getLogger('monitor_consumer')
logger.setLevel(logging.DEBUG)
logger.addHandler(LogHandler)

kafka_settings = parse_json_settings('config/kafka.json')

consumer = Consumer(
    kafka_settings['topic'],
    **kafka_settings.get('kwargs'),
)

psql = PSQL(**parse_json_settings('config/psql.json'))

with consumer and psql:
    connection = psql.connection()
    monitor_event = MonitorEvent(connection)

    logger.info("Daemon started, waiting for new messages.")

    for message in consumer.get():
        data = json.loads(message.value.decode("utf-8"))

        logger.debug('got message: {}'.format(str(message.value)))

        monitor_event.add(
            url=data.get('url'),
            status_code=data.get('status_code'),
            request_duration=data.get('request_duration'),
            created_at=data.get('created_at'),
            is_found=data.get('is_found'),
        )
