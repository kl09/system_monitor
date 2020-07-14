import logging

from monitor_producer.runner import Runner
from monitor_producer.producer import Producer
from monitor_producer.utils import LogHandler, parse_websites_settings, parse_json_settings

logger = logging.getLogger('monitor_producer')
logger.setLevel(logging.DEBUG)
logger.addHandler(LogHandler)

kafka_settings = parse_json_settings('config/kafka.json')

with Producer(**kafka_settings.get('kwargs')) as producer:
    Runner(
        sites=parse_websites_settings('config/websites.json'),
        producer=producer,
        topic=kafka_settings['topic'],
    ).run()
