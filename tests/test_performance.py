# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TransactionTestCase

from treenode.debug import debug_performance
from treenode.signals import no_signals

from .models import Category


class TreeNodePerformanceTestCase(TransactionTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_performance(self):
        settings.DEBUG = True
        debug_message_args = (Category.__module__, Category.__name__, )
        debug_message_prefix = '[treenode] create %s.%s tree: ' % debug_message_args
        with debug_performance(debug_message_prefix):
            with no_signals():
                for i in range(2000):
                    # cat_obj = Category.objects.create(
                    Category.objects.create(
                        name=str(i),
                        tn_parent=None,
                        tn_priority=0)
                    # cat_parent_obj = cat_obj
                    # for j in range(10):
                    #     subcat_obj = Category.objects.create(
                    #         name='%s - %s' % (str(cat_obj), str(j), ),
                    #         tn_parent=cat_parent_obj,
                    #         tn_priority=0)
                    #     cat_parent_obj = subcat_obj

        Category.update_tree()
        settings.DEBUG = False
