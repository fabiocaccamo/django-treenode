# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import TestCase

# from treenode.admin import TreeNodeModelAdmin


class TreeNodeAdminTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertStaticFile(self, path):
        result = finders.find(path)
        self.assertTrue(result != None)

    def test_staticfiles(self):
        if 'treenode' not in settings.INSTALLED_APPS:
            return
        self.assertStaticFile('treenode/css/treenode.css')
        self.assertStaticFile('treenode/js/treenode.js')
