# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import connection

import logging
import timeit


logger = logging.getLogger(__name__)


class debug_performance(object):

    def __init__(self, message_prefix=''):
        super(debug_performance, self).__init__()
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
        queries = (debug_performance._get_queries() - self.__init_queries)
        timer = (debug_performance._get_timer() - self.__init_timer)
        message = '\r%sexecuted %s %s in %ss.' % (
            self.__message_prefix,
            queries,
            'query' if queries == 1 else 'queries',
            timer, )
        logger.debug(message)
