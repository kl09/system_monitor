from datetime import timedelta
import re

import requests


class WebChecker:
    """WEB checker to check url status. """

    def check(self, url: str, regexp_pattern: str = '') -> (int, timedelta, bool):
        """
        Run web check by URL.

        :param url: url of website to check
        :param regexp_pattern: regexp pattern that is expected to be found on the page.
        :return: status_code, response time, existed_pattern
        """
        resp = requests.get(
            url=url,
            timeout=10,
        )

        found = bool(re.search(regexp_pattern, str(resp.content))) if regexp_pattern else False

        return resp.status_code, resp.elapsed.total_seconds(), found
