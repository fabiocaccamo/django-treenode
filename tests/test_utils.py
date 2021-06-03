# -*- coding: utf-8 -*-

from django.test import TestCase

from treenode.utils import join_pks, split_pks


class TreeNodeUtilsTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_join_pks(self):
        s = join_pks(None)
        self.assertEqual(s, '')
        s = join_pks([])
        self.assertEqual(s, '')
        s = join_pks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(s, '0,1,2,3,4,5,6,7,8,9,10')

    def test_split_pks(self):
        l = split_pks(None)
        self.assertEqual(l, [])
        l = split_pks('')
        self.assertEqual(l, [])
        l = split_pks('0,1,2,3,4,5,6,7,8,9,10')
        self.assertEqual(l, [str(i) for i in range(11)])
