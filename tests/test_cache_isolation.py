from django.test import TestCase

from tests.models import Category, CategoryFixtures
from treenode.cache import _get_cache, clear_cache, query_cache
from treenode.signals import no_signals


class TreeNodeCacheIsolationTestCase(TestCase):
    def setUp(self):
        Category.delete_tree()
        CategoryFixtures.delete_tree()

    def tearDown(self):
        Category.delete_tree()
        CategoryFixtures.delete_tree()

    def test_clearing_one_models_cache_does_not_touch_another_models(self):
        with no_signals():
            Category.objects.create(name="cat-a")
            CategoryFixtures.objects.create(name="fixture-a")
        Category.update_tree()
        CategoryFixtures.update_tree()

        # populate both models' caches
        category_cached = query_cache(Category)
        fixtures_cached = query_cache(CategoryFixtures)
        self.assertEqual(len(category_cached), 1)
        self.assertEqual(len(fixtures_cached), 1)

        # clearing Category's cache must not touch CategoryFixtures' entry
        clear_cache(Category)
        c = _get_cache()
        self.assertIsNone(c.get(f"treenode_list:{Category._meta.label_lower}"))
        self.assertIsNone(c.get(f"treenode_dict:{Category._meta.label_lower}"))
        self.assertIsNotNone(
            c.get(f"treenode_list:{CategoryFixtures._meta.label_lower}")
        )
        self.assertIsNotNone(
            c.get(f"treenode_dict:{CategoryFixtures._meta.label_lower}")
        )

        # and CategoryFixtures' cached data is still correct
        self.assertEqual(query_cache(CategoryFixtures), fixtures_cached)
