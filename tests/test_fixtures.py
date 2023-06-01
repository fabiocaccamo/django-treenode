from django.core.management import call_command
from django.test import TestCase

from .models import CategoryFixtures


class TreeNodeFixturesTestCase(TestCase):
    def test_loaddata_issue_0088(self):
        call_command("loaddata", "test_fixtures_issue_0088.json")
        self.assertEqual(CategoryFixtures.objects.count(), 19)
        expected_tree_display = """
Category pk=1
— Category pk=2
— — Category pk=3
— — — Category pk=4
— — — — Category pk=5
Category pk=6
— Category pk=7
— — Category pk=8
Category pk=9
— Category pk=10
— — Category pk=11
— — — Category pk=12
Category pk=28
— Category pk=29
— — Category pk=30
— — — Category pk=24
Category pk=31
— Category pk=32
— — Category pk=33
""".strip()
        self.assertEqual(CategoryFixtures.get_tree_display(), expected_tree_display)
