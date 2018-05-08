# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import connection

import logging
import timeit


logger = logging.getLogger(__name__)


class debug_performance():

    def __get_queries(self):
        return len(connection.queries)

    def __get_timer(self):
        return timeit.default_timer()

    def __enter__(self):
        self.__init_queries = self.__get_queries()
        self.__init_timer = self.__get_timer()
        return None

    def __exit__(self, type, value, traceback):
        queries = (self.__get_queries() - self.__init_queries)
        timer = (self.__get_timer() - self.__init_timer)
        if settings.DEBUG:
            message = '\rExecuted %s %s in %ss.' % (
                queries, 'query' if queries == 1 else 'queries', timer, )
            print(message)
