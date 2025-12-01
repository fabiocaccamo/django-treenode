from django.test import TestCase

from tests.models import Category
from treenode.exceptions import CircularReferenceError


class TreeNodeParentValidationTestCase(TestCase):
    def setUp(self):
        self.root_a = Category.objects.create(name="Root A")
        self.child_aa = Category.objects.create(name="Child AA", tn_parent=self.root_a)
        self.child_ab = Category.objects.create(name="Child AB", tn_parent=self.root_a)
        self.grandchild_aaa = Category.objects.create(
            name="Grandchild AAA", tn_parent=self.child_aa
        )

        Category.update_tree()

        self.root_a.refresh_from_db()
        self.child_aa.refresh_from_db()
        self.child_ab.refresh_from_db()
        self.grandchild_aaa.refresh_from_db()

    def tearDown(self):
        Category.delete_tree()

    def test_valid_tree_structure_creation(self):
        a = Category.objects.create(name="A")
        aa = Category.objects.create(name="AA", tn_parent=a)
        ab = Category.objects.create(name="AB", tn_parent=a)
        aaa = Category.objects.create(name="AAA", tn_parent=aa)

        Category.update_tree()

        self.assertEqual(Category.objects.count(), 8)

        a.refresh_from_db()
        aa.refresh_from_db()
        ab.refresh_from_db()
        aaa.refresh_from_db()

        self.assertEqual(a.tn_children_count, 2)
        self.assertEqual(aa.tn_children_count, 1)
        self.assertEqual(ab.tn_children_count, 0)
        self.assertEqual(aaa.tn_children_count, 0)

        self.assertEqual(a.tn_ancestors_count, 0)
        self.assertEqual(aa.tn_ancestors_count, 1)
        self.assertEqual(ab.tn_ancestors_count, 1)
        self.assertEqual(aaa.tn_ancestors_count, 2)

        self.assertEqual(a.tn_level, 1)
        self.assertEqual(aa.tn_level, 2)
        self.assertEqual(ab.tn_level, 2)
        self.assertEqual(aaa.tn_level, 3)

    def test_empty_tree_validation(self):
        Category.delete_tree()
        self.assertEqual(Category.objects.count(), 0)

        Category.update_tree()
        self.assertEqual(Category.objects.count(), 0)

    def test_single_node_validation(self):
        Category.delete_tree()
        a = Category.objects.create(name="A")
        Category.update_tree()

        a.refresh_from_db()

        self.assertEqual(a.tn_ancestors_count, 0)
        self.assertEqual(a.tn_children_count, 0)
        self.assertEqual(a.tn_level, 1)
        self.assertEqual(a.tn_order, 0)
        self.assertEqual(a.tn_siblings_count, 0)
        self.assertTrue(a.is_root())
        self.assertTrue(a.is_leaf())

    def test_parent_relationship_data_retrieval(self):
        objs_qs = Category.objects.select_related("tn_parent")
        self.assertIsNotNone(objs_qs)

        objs_list = list(objs_qs)
        self.assertEqual(len(objs_list), 4)
        self.assertIn(self.root_a, objs_list)
        self.assertIn(self.child_aa, objs_list)
        self.assertIn(self.child_ab, objs_list)
        self.assertIn(self.grandchild_aaa, objs_list)

        objs_dict = {str(obj.pk): obj for obj in objs_list}
        self.assertEqual(len(objs_dict), 4)
        self.assertIn(str(self.root_a.pk), objs_dict)
        self.assertIn(str(self.child_aa.pk), objs_dict)
        self.assertIn(str(self.child_ab.pk), objs_dict)
        self.assertIn(str(self.grandchild_aaa.pk), objs_dict)

        self.assertEqual(objs_dict[str(self.root_a.pk)], self.root_a)
        self.assertEqual(objs_dict[str(self.child_aa.pk)], self.child_aa)
        self.assertEqual(objs_dict[str(self.child_ab.pk)], self.child_ab)
        self.assertEqual(objs_dict[str(self.grandchild_aaa.pk)], self.grandchild_aaa)

        self.assertIsNone(objs_dict[str(self.root_a.pk)].tn_parent)
        self.assertEqual(objs_dict[str(self.child_aa.pk)].tn_parent, self.root_a)
        self.assertEqual(objs_dict[str(self.child_ab.pk)].tn_parent, self.root_a)
        self.assertEqual(
            objs_dict[str(self.grandchild_aaa.pk)].tn_parent, self.child_aa
        )

    def test_parent_dependency_attributes_validation(self):
        objs_qs = Category.objects.select_related("tn_parent")
        objs_list = list(objs_qs)
        objs_dict = {str(obj.pk): obj for obj in objs_list}

        for obj in objs_dict.values():
            self.assertTrue(hasattr(obj, "tn_parent"))
            self.assertTrue(hasattr(obj, "tn_children_count"))
            self.assertTrue(hasattr(obj, "tn_ancestors_count"))
            self.assertTrue(hasattr(obj, "tn_level"))

            if obj.tn_ancestors_count == 0:
                self.assertIsNone(obj.tn_parent)
            else:
                self.assertIsNotNone(obj.tn_parent)

    def test_parent_dependency_data_integrity(self):
        objs_qs = Category.objects.select_related("tn_parent")
        objs_list = list(objs_qs)
        objs_dict = {str(obj.pk): obj for obj in objs_list}

        self.assertEqual(objs_qs.count(), 4)
        self.assertTrue(hasattr(objs_qs.first(), "tn_parent"))

        self.assertEqual(len(objs_list), 4)
        self.assertIn(self.root_a, objs_list)
        self.assertIn(self.child_aa, objs_list)
        self.assertIn(self.child_ab, objs_list)
        self.assertIn(self.grandchild_aaa, objs_list)

        self.assertEqual(len(objs_dict), 4)
        self.assertIn(str(self.root_a.pk), objs_dict)
        self.assertIn(str(self.child_aa.pk), objs_dict)
        self.assertIn(str(self.child_ab.pk), objs_dict)
        self.assertIn(str(self.grandchild_aaa.pk), objs_dict)

        self.assertEqual(objs_dict[str(self.root_a.pk)], self.root_a)
        self.assertEqual(objs_dict[str(self.child_aa.pk)], self.child_aa)
        self.assertEqual(objs_dict[str(self.child_ab.pk)], self.child_ab)
        self.assertEqual(objs_dict[str(self.grandchild_aaa.pk)], self.grandchild_aaa)

        self.assertIsNone(objs_dict[str(self.root_a.pk)].tn_parent)
        self.assertEqual(objs_dict[str(self.child_aa.pk)].tn_parent, self.root_a)
        self.assertEqual(objs_dict[str(self.child_ab.pk)].tn_parent, self.root_a)
        self.assertEqual(
            objs_dict[str(self.grandchild_aaa.pk)].tn_parent, self.child_aa
        )

    def test_self_reference_circular_dependency_detection(self):
        Category.delete_tree()
        a = Category.objects.create(name="A")

        with self.assertRaises(CircularReferenceError):
            a.tn_parent = a
            a.save()
            Category.update_tree()

    def test_mutual_reference_circular_dependency_detection(self):
        Category.delete_tree()
        a = Category.objects.create(name="A")
        b = Category.objects.create(name="B", tn_parent=a)
        Category.update_tree()

        with self.assertRaises(CircularReferenceError):
            a.tn_parent = b
            a.save()
            Category.update_tree()

    def test_valid_parent_child_relationship_validation(self):
        Category.delete_tree()
        a = Category.objects.create(name="A")
        b = Category.objects.create(name="B", tn_parent=a)
        c = Category.objects.create(name="C", tn_parent=b)

        try:
            Category.update_tree()
        except CircularReferenceError:
            self.fail(
                "Valid parent-child relationships should not raise "
                "circular reference error"
            )

        a.refresh_from_db()
        b.refresh_from_db()
        c.refresh_from_db()

        self.assertIsNone(a.tn_parent)
        self.assertEqual(b.tn_parent, a)
        self.assertEqual(c.tn_parent, b)

    def test_direct_circular_dependency_detection_via_update_tree(self):
        Category.delete_tree()
        a = Category.objects.create(name="A")
        b = Category.objects.create(name="B", tn_parent=a)

        # bypass post_save signal
        Category.objects.filter(pk=a.pk).update(tn_parent=b)

        with self.assertRaises(CircularReferenceError):
            Category.update_tree()
