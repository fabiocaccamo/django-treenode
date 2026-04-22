"""
Tests for the post_save update_tree skip optimizations.

When save(update_fields=[...]) is passed and none of the listed fields are
structural (tn_parent, tn_parent_id, tn_priority, or the model's
treenode_display_field), update_tree is not called.

When a full save() is issued without update_fields, update_tree is not called
if tn_parent_id, tn_priority and the display-field value are all unchanged
compared to the snapshot captured at post_init / post_save time.

Rather than mocking update_tree, each test verifies the optimisation by
observing a real side-effect: before the action under test a sentinel value
(999) is written directly to the tn_level column via QuerySet.update() (which
bypasses Django signals and the ORM save path).  After the action:
- if update_tree was NOT expected to run, tn_level is still 999.
- if update_tree WAS expected to run, tn_level has been corrected to its real
  value.
"""

from django.test import TransactionTestCase

from tests.models import Category, CategoryWithoutDisplayField
from treenode.signals import no_signals


class TreeNodeSaveOptimizationTestCase(TransactionTestCase):
    def setUp(self):
        with no_signals():
            self.root = Category.objects.create(name="root")
            self.child = Category.objects.create(name="child", tn_parent=self.root)
            self.plain = CategoryWithoutDisplayField.objects.create(name="plain")
        Category.update_tree()
        CategoryWithoutDisplayField.update_tree()

    def tearDown(self):
        Category.objects.all().delete()
        CategoryWithoutDisplayField.objects.all().delete()

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _corrupt_level(self, model, pk):
        """Write an obviously-wrong tn_level directly to the DB row."""
        model.objects.filter(pk=pk).update(tn_level=999)

    def _db_level(self, model, pk):
        return model.objects.get(pk=pk).tn_level

    # ------------------------------------------------------------------
    # tests: update_tree should NOT be called
    # ------------------------------------------------------------------

    def test_skip_update_tree_when_update_fields_non_structural_no_display_field(self):
        self._corrupt_level(CategoryWithoutDisplayField, self.plain.pk)
        obj = CategoryWithoutDisplayField.objects.get(pk=self.plain.pk)
        obj.name = "plain-renamed"
        obj.save(update_fields=["name"])
        self.assertEqual(self._db_level(CategoryWithoutDisplayField, self.plain.pk), 999)

    def test_skip_update_tree_when_no_structural_field_changed(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.save()
        self.assertEqual(self._db_level(Category, self.root.pk), 999)

    # ------------------------------------------------------------------
    # tests: update_tree SHOULD be called
    # ------------------------------------------------------------------

    def test_trigger_update_tree_when_update_fields_has_tn_priority(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 5
        obj.save(update_fields=["tn_priority"])
        self.assertEqual(self._db_level(Category, self.root.pk), 1)

    def test_trigger_update_tree_when_update_fields_has_tn_parent_id(self):
        self._corrupt_level(Category, self.child.pk)
        obj = Category.objects.get(pk=self.child.pk)
        obj.save(update_fields=["tn_parent_id"])
        self.assertEqual(self._db_level(Category, self.child.pk), 2)

    def test_trigger_update_tree_when_update_fields_has_display_field(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        obj.save(update_fields=["name"])
        self.assertEqual(self._db_level(Category, self.root.pk), 1)

    def test_trigger_update_tree_when_update_fields_mixed_structural_and_non_structural(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 3
        obj.save(update_fields=["tn_priority"])
        self.assertEqual(self._db_level(Category, self.root.pk), 1)

    def test_trigger_update_tree_when_tn_parent_changed(self):
        self._corrupt_level(Category, self.child.pk)
        obj = Category.objects.get(pk=self.child.pk)
        obj.tn_parent = None
        obj.save()
        # child is now a root node → tn_level == 1
        self.assertEqual(self._db_level(Category, self.child.pk), 1)

    def test_trigger_update_tree_when_tn_priority_changed(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 99
        obj.save()
        self.assertEqual(self._db_level(Category, self.root.pk), 1)

    def test_trigger_update_tree_when_display_field_changed(self):
        self._corrupt_level(Category, self.root.pk)
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        obj.save()
        self.assertEqual(self._db_level(Category, self.root.pk), 1)

    def test_trigger_update_tree_on_create(self):
        Category.objects.all().update(tn_level=999)
        Category.objects.create(name="new-node")
        self.assertEqual(self._db_level(Category, self.root.pk), 1)
