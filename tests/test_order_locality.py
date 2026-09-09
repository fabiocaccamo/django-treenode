from django.test import TestCase

from tests.models import Category
from treenode.signals import no_signals


class TreeNodeOrderLocalityTestCase(TestCase):
    """
    Regression test for the bug described in
    docs/superpowers/specs/2026-08-26-local-order-key-design.md:
    tn_order used to be a dense rank over the WHOLE table, so inserting a
    node in one tree could shift the tn_order of every node in every other,
    unrelated tree. This pins down that inserting into tree0 must not touch
    tree1's tn_order values at all.
    """

    def setUp(self):
        Category.delete_tree()

    def test_inserting_a_node_does_not_change_order_of_other_trees(self):
        with no_signals():
            tree0_root = Category.objects.create(name="tree0-root")
            Category.objects.create(name="tree0-a", tn_parent=tree0_root)
            Category.objects.create(name="tree0-b", tn_parent=tree0_root)

            tree1_root = Category.objects.create(name="tree1-root")
            Category.objects.create(name="tree1-a", tn_parent=tree1_root)
            Category.objects.create(name="tree1-b", tn_parent=tree1_root)
        Category.update_tree()

        def tree1_orders():
            return {
                obj.name: obj.tn_order
                for obj in Category.objects.filter(name__startswith="tree1-")
            }

        orders_before = tree1_orders()
        # Guard against the name filter silently matching nothing (which
        # would make the assertion below pass vacuously).
        self.assertEqual(len(orders_before), 3)

        # Inserted alphabetically between "tree0-b" and "tree0-root", so
        # under the old dense-global-rank scheme this would shift the rank
        # of tree0-root and everything that sorts after it -- including
        # all of tree1.
        Category.objects.create(name="tree0-c", tn_parent=tree0_root)

        orders_after = tree1_orders()

        self.assertEqual(orders_before, orders_after)

    def test_inserting_a_new_root_does_not_change_order_of_other_trees(self):
        """
        tn_order is built from each node's own stable order key (priority
        + slug + pk), chained with its ancestors', not from a
        position-derived rank. A new root's order key doesn't depend on
        any other root's, so inserting one -- even alphabetically before
        existing roots -- must not change tn_order anywhere else in the
        table, including inside unrelated trees.
        """
        with no_signals():
            tree1_root = Category.objects.create(name="tree1-root")
            Category.objects.create(name="tree1-a", tn_parent=tree1_root)
            Category.objects.create(name="tree1-b", tn_parent=tree1_root)
        Category.update_tree()

        def tree1_orders():
            return {
                obj.name: obj.tn_order
                for obj in Category.objects.filter(name__startswith="tree1-")
            }

        orders_before = tree1_orders()
        self.assertEqual(len(orders_before), 3)

        # Sorts alphabetically before "tree1-root".
        Category.objects.create(name="a-new-root")

        orders_after = tree1_orders()

        self.assertEqual(orders_before, orders_after)
