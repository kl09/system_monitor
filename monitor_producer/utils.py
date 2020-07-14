import logging
import datetime
import json

from dataclasses import dataclass


@dataclass
class Website:
    """Website struct for websites."""
    url: str
    check_interval: int
    regexp_pattern: str

    @property
    def code(self) -> str:
        """
        Return code of website.
        :return:
        """
        return '%s_%d_%s' % (self.url, self.check_interval, self.regexp_pattern)


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


def parse_json_settings(file: str):
    """
    Parse json settings from file.
    :param file: File path.
    :return:
    """
    with open(file) as f:
        return json.load(f)


def parse_websites_settings(file: str):
    """
    Parse websites   settings from file.
    :param file: File path.
    :return:
    """
    with open(file) as f:
        data = json.load(f)

        return mapping_to_website(data)


def mapping_to_website(data: list) -> [Website]:
    """
    Mapping map data to Website structs.
    :param data:
    :return:
    """
    return [
        Website(
            url=site['url'],
            check_interval=site['check_interval'],
            regexp_pattern=site['regexp_pattern'],
        ) for site in data
    ]
