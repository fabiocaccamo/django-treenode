from django.core.management import call_command
from django.test import TestCase

from .models import CategoryFixtures


class TreeNodeFixturesTestCase(TestCase):
    def test_loaddata_issue_0088(self):
        call_command("loaddata", "test_fixtures_issue_0088.json")
        self.assertEqual(CategoryFixtures.objects.count(), 19)
