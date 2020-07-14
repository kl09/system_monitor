import logging
import json
import datetime


def parse_json_settings(file: str):
    """
    Parse json settings from file.
    :param file: File path.
    :return:
    """
    with open(file) as f:
        return json.load(f)


class LogHandler:
    """Handler for logs."""
    level = logging.NOTSET

    @classmethod
    def handle(cls, record):
        """
        Handle function for logs.
        :param record:
        :return:
        """
        print(datetime.datetime.now(), record, flush=True)
