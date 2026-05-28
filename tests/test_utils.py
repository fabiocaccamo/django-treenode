from django.test import TestCase

from treenode.utils import contains_pk, join_pks, split_pks


class TreeNodeUtilsTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_contains_pk(self):
        self.assertEqual(contains_pk(None, 1), False)
        self.assertEqual(contains_pk("", 1), False)
        self.assertEqual(contains_pk("0", 1), False)
        self.assertEqual(contains_pk("1", 1), True)
        self.assertEqual(contains_pk("0,1", 1), True)
        self.assertEqual(contains_pk("0,1,2", 1), True)
        self.assertEqual(contains_pk("0,2,3", 1), False)

    def test_join_pks(self):
        pks_str = join_pks(None)
        self.assertEqual(pks_str, "")
        pks_str = join_pks([])
        self.assertEqual(pks_str, "")
        pks_str = join_pks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(pks_str, "0,1,2,3,4,5,6,7,8,9,10")

    def test_split_pks(self):
        pks_list = split_pks(None)
        self.assertEqual(pks_list, [])
        pks_list = split_pks("")
        self.assertEqual(pks_list, [])
        pks_list = split_pks("0,1,2,3,4,5,6,7,8,9,10")
        self.assertEqual(pks_list, [str(i) for i in range(11)])
