"""
Tests for the post_save update_tree skip optimizations.

When save(update_fields=[...]) is passed and none of the listed fields are
structural (tn_parent, tn_parent_id, tn_priority, or the model's
treenode_display_field), update_tree is not called.

When a full save() is issued without update_fields, update_tree is not called
if tn_parent_id, tn_priority and the display-field value are all unchanged
compared to the snapshot captured at post_init time.
"""

from unittest.mock import patch

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

    def test_skip_update_tree_when_update_fields_non_structural_no_display_field(self):
        obj = CategoryWithoutDisplayField.objects.get(pk=self.plain.pk)
        obj.name = "plain-renamed"
        with patch.object(CategoryWithoutDisplayField, "update_tree") as mock:
            obj.save(update_fields=["name"])
        mock.assert_not_called()

    def test_trigger_update_tree_when_update_fields_has_tn_priority(self):
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 5
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_priority"])
        mock.assert_called_once()

    def test_trigger_update_tree_when_update_fields_has_tn_parent_id(self):
        obj = Category.objects.get(pk=self.child.pk)
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_parent_id"])
        mock.assert_called_once()

    def test_trigger_update_tree_when_update_fields_has_display_field(self):
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["name"])
        mock.assert_called_once()

    def test_trigger_update_tree_when_update_fields_mixed_structural_and_non_structural(self):
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 3
        with patch.object(Category, "update_tree") as mock:
            obj.save(update_fields=["tn_priority"])
        mock.assert_called_once()

    def test_skip_update_tree_when_no_structural_field_changed(self):
        obj = Category.objects.get(pk=self.root.pk)
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_not_called()

    def test_trigger_update_tree_when_tn_parent_changed(self):
        obj = Category.objects.get(pk=self.child.pk)
        obj.tn_parent = None
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_trigger_update_tree_when_tn_priority_changed(self):
        obj = Category.objects.get(pk=self.root.pk)
        obj.tn_priority = 99
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_trigger_update_tree_when_display_field_changed(self):
        obj = Category.objects.get(pk=self.root.pk)
        obj.name = "root-renamed"
        with patch.object(Category, "update_tree") as mock:
            obj.save()
        mock.assert_called_once()

    def test_trigger_update_tree_on_create(self):
        with patch.object(Category, "update_tree") as mock:
            Category.objects.create(name="new-node")
        mock.assert_called_once()
