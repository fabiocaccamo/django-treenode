import logging
import timeit

from django.conf import settings
from django.db import connection

logger = logging.getLogger(__name__)


class debug_performance:
    def __init__(self, message_prefix=""):
        super().__init__()
        self.__message_prefix = message_prefix

    @staticmethod
    def _get_queries():
        return len(connection.queries)

    @staticmethod
    def _get_timer():
        return timeit.default_timer()

    def __enter__(self):
        if not settings.DEBUG:
            return None
        self.__init_queries = debug_performance._get_queries()
        self.__init_timer = debug_performance._get_timer()
        return None

    def __exit__(self, type_, value, traceback):
        if not settings.DEBUG:
            return
        prefix = self.__message_prefix
        queries = debug_performance._get_queries() - self.__init_queries
        queries_label = "query" if queries == 1 else "queries"
        timer = debug_performance._get_timer() - self.__init_timer
        message = f"\r{prefix}executed {queries} {queries_label} in {timer}s."
        logger.debug(message)
