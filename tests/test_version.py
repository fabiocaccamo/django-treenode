# -*- coding: utf-8 -*-

import re

from django.test import TestCase

from treenode.version import __version__


class TreeNodeVersionTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        v = __version__
        self.assertTrue(v != None)
        self.assertTrue(v != "")
        v_re = re.compile(r"^([0-9]+)(\.([0-9]+)){1,2}$")
        v_match = v_re.match(v)
        self.assertTrue(v_match != None)
