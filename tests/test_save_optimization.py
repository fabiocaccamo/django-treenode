"""
Tests for the post_save update_tree skip optimizations:

1A – when save(update_fields=[...]) is passed and none of the listed fields
     are structural (tn_parent, tn_parent_id, tn_priority, or the model's
     treenode_display_field), update_tree must NOT be called.

1B – when a full save() is issued without update_fields, update_tree must NOT
     be called if tn_parent_id, tn_priority and the display-field value are all
     unchanged compared to the snapshot captured at post_init time.
"""

from unittest.mock import patch

from django.test import TransactionTestCase

from tests.models import Category, CategoryWithoutDisplayField
from treenode.signals import no_signals


class TreeNodeSaveOptimizationTestCase(TransactionTestCase):
    def setUp(self):
        # Create objects without triggering signals so that each individual
        # test controls exactly when update_tree is expected to run.
        with no_signals():
            self.root = Category.objects.create(name="root")
            self.child = Category.objects.create(name="child", tn_parent=self.root)
            self.plain = CategoryWithoutDisplayField.objects.create(name="plain")
        Category.update_tree()
        CategoryWithoutDisplayField.update_tree()

    def tearDown(self):
        Category.objects.all().delete()
        CategoryWithoutDisplayField.objects.all().delete()

    # ------------------------------------------------------------------ 1A ---

    def test_1a_skip_when_update_fields_non_structural_no_display_field(self):
        """No display_field model: update_fields=['name'] must skip update_tree."""
        obj = CategoryWithoutDisplayField.objects.get(pk=self.plain.pk)
        obj.name = "plain-renamed"
        with patch.object(CategoryWithoutDisplayField, "update_tree") as mock:
            obj.save(update_fields=["name"])
        mock.assert_not_called()

    def test_1a_trigger_when_update_fields_has_tn_priority(self):
        """update_fields=['tn_priority'] must call update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 5
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_priority"])
        mock.assert_called_once()

    def test_1a_trigger_when_update_fields_has_tn_parent_id(self):
        """update_fields=['tn_parent_id'] must call update_tree."""
        obj = Category.objects.get(pk=self.child.pk)
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_parent_id"])
        mock.assert_called_once()

    def test_1a_trigger_when_update_fields_has_display_field(self):
        """For Category (display_field='name'), update_fields=['name'] must call update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["name"])
        mock.assert_called_once()

    def test_1a_trigger_when_update_fields_mixed_structural_and_non_structural(self):
        """update_fields containing at least one structural field must call update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 3
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_priority"])
        mock.assert_called_once()

    # ------------------------------------------------------------------ 1B ---

    def test_1b_skip_when_no_structural_field_changed(self):
        """Full save() with no structural change must skip update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        # Do not touch tn_parent_id, tn_priority, or name (the display field).
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_not_called()

    def test_1b_trigger_when_tn_parent_changed(self):
        """Full save() after changing tn_parent must call update_tree."""
        obj = Category.objects.get(pk=self.child.pk)
        obj.tn_parent = None
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_1b_trigger_when_tn_priority_changed(self):
        """Full save() after changing tn_priority must call update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 99
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_1b_trigger_when_display_field_changed(self):
        """Full save() after changing treenode_display_field value must call update_tree."""
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_1b_trigger_on_create(self):
        """Creating a new object must always call update_tree regardless of snapshot."""
        with patch.object(Category, "update_tree") as mock:
            Category.objects.create(name="new-node")
        mock.assert_called_once()
