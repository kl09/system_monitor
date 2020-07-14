import datetime


class MonitorEvent:
    """
    MonitorEvent is a storage for monitor events.
    """

    def __init__(self, connect):
        """
        Creates a MonitorEvent object.

        :param connect: Connection to repository with cursor.
        """
        if not hasattr(connect, 'cursor'):
            raise Exception("Expected connect with cursor")

        self.connect = connect

    def add(self, url: str, status_code: int, request_duration: float, created_at: datetime, is_found: bool):
        """
        Creates monitor events information to repository.

        :param url: URL of website.
        :param status_code: Status code of request.
        :param request_duration: Time of request duration.
        :param created_at: Created at.
        :param is_found: Is the content was found.
        :return:
        """

        with self.connect.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO system_monitor_events
                (
                    url,
                    status_code,
                    request_duration,
                    is_content_found,
                    created_at
                )
                VALUES
                (%s, %s, %s, %s, %s);
            """,
                (url, status_code, request_duration, is_found, created_at),
            )
