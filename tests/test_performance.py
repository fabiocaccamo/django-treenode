from django.conf import settings
from django.db import connection
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext

from tests.models import Category
from treenode.debug import debug_performance
from treenode.signals import no_signals


class TreeNodePerformanceTestCase(TransactionTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_performance(self):
        settings.DEBUG = True
        message_prefix = (
            f"[treenode] create {Category.__module__}.{Category.__name__} tree: "
        )
        with debug_performance(message_prefix=message_prefix):
            with no_signals():
                for i in range(2000):
                    # cat_obj = Category.objects.create(
                    Category.objects.create(name=f"{i}", tn_parent=None, tn_priority=0)
                    # cat_parent_obj = cat_obj
                    # for j in range(10):
                    #     subcat_obj = Category.objects.create(
                    #         name=f"{cat_obj} - {j}",
                    #         tn_parent=cat_parent_obj,
                    #         tn_priority=0,
                    #     )
                    #     cat_parent_obj = subcat_obj

        Category.update_tree()
        settings.DEBUG = False

    def test_update_tree_uses_bulk_updates(self):
        with no_signals():
            root = Category.objects.create(name="root")
            for i in range(7):
                child = Category.objects.create(name=f"child-{i}", tn_parent=root)
                for j in range(6):
                    Category.objects.create(name=f"child-{i}-{j}", tn_parent=child)

        with CaptureQueriesContext(connection) as ctx:
            Category.update_tree()

        # updates must be batched, not issued per-row (50 nodes)
        self.assertLessEqual(len(ctx.captured_queries), 10)
