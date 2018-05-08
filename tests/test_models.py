# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings

from treenode.utils import join_pks, split_pks

from .models import Category


class TreeNodeModelsTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def __create_cat(self, name, parent=None, priority=0):
        return Category.objects.create(
            name=name,
            tn_parent=parent,
            tn_priority=priority)

    def __create_cat_tree(self):
        """
            a
                aa
                    aaa
                        aaaa
                ab
                ac
                    aca
                        acaa
                        acab
                    acb
                    acc
                ad
                ae
                af
            b
                ba
                bb
                bc
            c
            d
            e
            f
        """
        a = self.__create_cat(name='a')
        aa = self.__create_cat(name='aa', parent=a)
        aaa = self.__create_cat(name='aaa', parent=aa)
        aaaa = self.__create_cat(name='aaaa', parent=aaa)
        ab = self.__create_cat(name='ab', parent=a)
        ac = self.__create_cat(name='ac', parent=a)
        aca = self.__create_cat(name='aca', parent=ac)
        acaa = self.__create_cat(name='acaa', parent=aca)
        acab = self.__create_cat(name='acab', parent=aca)
        acb = self.__create_cat(name='acb', parent=ac)
        acc = self.__create_cat(name='acc', parent=ac)
        ad = self.__create_cat(name='ad', parent=a)
        ae = self.__create_cat(name='ae', parent=a)
        af = self.__create_cat(name='af', parent=a)
        b = self.__create_cat(name='b')
        ba = self.__create_cat(name='ba', parent=b)
        bb = self.__create_cat(name='bb', parent=b)
        bc = self.__create_cat(name='bc', parent=b)
        c = self.__create_cat(name='c')
        d = self.__create_cat(name='d')
        e = self.__create_cat(name='e')
        f = self.__create_cat(name='f')

    def __get_cat(self, name):
        return Category.objects.get(name=name)

    def test_delete(self):
        self.__create_cat_tree()
        # settings.DEBUG = True
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        a.delete()
        a.delete()
        self.assertEqual(Category.get_roots(), [b, c, d, e, f])
        # settings.DEBUG = False

    def test_delete_all(self):
        self.__create_cat_tree()
        # settings.DEBUG = True
        Category.delete_all()
        self.assertEqual(list(Category.objects.all()), [])
        # settings.DEBUG = False

    def test_get_ancestors(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(aaaa.tn_ancestors_pks, join_pks([a.pk, aa.pk, aaa.pk]))
        self.assertEqual(aaaa.get_ancestors(), [a, aa, aaa])

    def test_get_ancestors_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_ancestors_count(), 0)
        self.assertEqual(aa.get_ancestors_count(), 1)
        self.assertEqual(aaa.get_ancestors_count(), 2)
        self.assertEqual(aaaa.get_ancestors_count(), 3)

    def test_get_children(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(a.tn_children_pks, join_pks([aa.pk, ab.pk, ac.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(a.get_children(), [aa, ab, ac, ad, ae, af])

    def test_get_children_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        self.assertEqual(a.tn_children_count, 6)
        self.assertEqual(a.get_children_count(), 6)

    def test_get_depth(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_depth(), 3)
        self.assertEqual(aa.get_depth(), 2)
        self.assertEqual(aaa.get_depth(), 1)
        self.assertEqual(aaaa.get_depth(), 0)

    def test_get_descendants(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        aca = self.__get_cat(name='aca')
        acaa = self.__get_cat(name='acaa')
        acab = self.__get_cat(name='acab')
        acb = self.__get_cat(name='acb')
        acc = self.__get_cat(name='acc')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(a.get_descendants(),
            [aa, aaa, aaaa, ab, ac, aca, acaa, acab, acb, acc, ad, ae, af])
        self.assertEqual(aa.get_descendants(), [aaa, aaaa])
        self.assertEqual(aaa.get_descendants(), [aaaa])
        self.assertEqual(aaaa.get_descendants(), [])

    def test_get_descendants_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_descendants_count(), 13)
        self.assertEqual(aa.get_descendants_count(), 2)
        self.assertEqual(aaa.get_descendants_count(), 1)
        self.assertEqual(aaaa.get_descendants_count(), 0)

    def test_get_descendants_tree(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        aca = self.__get_cat(name='aca')
        acaa = self.__get_cat(name='acaa')
        acab = self.__get_cat(name='acab')
        acb = self.__get_cat(name='acb')
        acc = self.__get_cat(name='acc')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        b = self.__get_cat(name='b')
        ba = self.__get_cat(name='ba')
        bb = self.__get_cat(name='bb')
        bc = self.__get_cat(name='bc')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        tree = [
            {
                'node': aca,
                'tree': [
                    {
                        'node': acaa,
                        'tree': [],
                    },
                    {
                        'node': acab,
                        'tree': [],
                    },
                ],
            },
            {
                'node': acb,
                'tree': [],
            },
            {
                'node': acc,
                'tree': [],
            },
        ]
        self.assertEqual(tree, ac.get_descendants_tree())
        tree = [
            {
                'node': ba,
                'tree': [],
            },
            {
                'node': bb,
                'tree': [],
            },
            {
                'node': bc,
                'tree': [],
            },
        ]
        self.assertEqual(tree, b.get_descendants_tree())
        tree = [
        ]
        self.assertEqual(tree, c.get_descendants_tree())

    def test_get_descendants_tree_display(self):
        # TODO
        pass

    def test_get_index(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.get_index(), 0)
        self.assertEqual(aa.get_index(), 0)
        self.assertEqual(aaa.get_index(), 0)
        self.assertEqual(aaaa.get_index(), 0)
        self.assertEqual(ab.get_index(), 1)
        self.assertEqual(ac.get_index(), 2)
        self.assertEqual(ad.get_index(), 3)
        self.assertEqual(ae.get_index(), 4)
        self.assertEqual(af.get_index(), 5)
        self.assertEqual(b.get_index(), 1)
        self.assertEqual(c.get_index(), 2)
        self.assertEqual(d.get_index(), 3)
        self.assertEqual(e.get_index(), 4)
        self.assertEqual(f.get_index(), 5)

    def test_get_level(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_level(), 1)
        self.assertEqual(aa.get_level(), 2)
        self.assertEqual(aaa.get_level(), 3)
        self.assertEqual(aaaa.get_level(), 4)

    def test_get_order(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        aca = self.__get_cat(name='aca')
        acaa = self.__get_cat(name='acaa')
        acab = self.__get_cat(name='acab')
        acb = self.__get_cat(name='acb')
        acc = self.__get_cat(name='acc')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        b = self.__get_cat(name='b')
        ba = self.__get_cat(name='ba')
        bb = self.__get_cat(name='bb')
        bc = self.__get_cat(name='bc')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.get_order(), 0)
        self.assertEqual(aa.get_order(), 1)
        self.assertEqual(aaa.get_order(), 2)
        self.assertEqual(aaaa.get_order(), 3)
        self.assertEqual(ab.get_order(), 4)
        self.assertEqual(ac.get_order(), 5)
        self.assertEqual(aca.get_order(), 6)
        self.assertEqual(acaa.get_order(), 7)
        self.assertEqual(acab.get_order(), 8)
        self.assertEqual(acb.get_order(), 9)
        self.assertEqual(acc.get_order(), 10)
        self.assertEqual(ad.get_order(), 11)
        self.assertEqual(ae.get_order(), 12)
        self.assertEqual(af.get_order(), 13)
        self.assertEqual(b.get_order(), 14)
        self.assertEqual(ba.get_order(), 15)
        self.assertEqual(bb.get_order(), 16)
        self.assertEqual(bc.get_order(), 17)
        self.assertEqual(c.get_order(), 18)
        self.assertEqual(d.get_order(), 19)
        self.assertEqual(e.get_order(), 20)
        self.assertEqual(f.get_order(), 21)

    def test_get_parent(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_parent(), None)
        self.assertEqual(aa.get_parent(), a)
        self.assertEqual(aaa.get_parent(), aa)
        self.assertEqual(aaaa.get_parent(), aaa)

    def test_set_parent(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        with self.assertRaises(ValueError):
            a.set_parent(a)
        # with self.assertRaises(ValueError):
        #     a.set_parent(aa)
        d.set_parent(c)
        e.set_parent(c)
        f.set_parent(c)
        self.assertEqual(d.tn_ancestors_pks, join_pks([c.pk]))
        self.assertEqual(d.get_parent(), c)
        self.assertEqual(e.tn_ancestors_pks, join_pks([c.pk]))
        self.assertEqual(e.get_parent(), c)
        self.assertEqual(f.tn_ancestors_pks, join_pks([c.pk]))
        self.assertEqual(f.get_parent(), c)
        self.assertEqual(c.tn_children_pks, join_pks([d.pk, e.pk, f.pk]))
        self.assertEqual(c.get_children(), [d, e, f])

    def test_set_parent_none(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        a.set_parent(None)
        aa.set_parent(None)
        aaa.set_parent(None)
        aaaa.set_parent(None)
        self.assertTrue(a.is_root())
        self.assertEqual(a.get_ancestors_count(), 0)
        self.assertEqual(a.get_parent(), None)
        self.assertTrue(aa.is_root())
        self.assertEqual(aa.get_ancestors_count(), 0)
        self.assertEqual(aa.get_parent(), None)
        self.assertTrue(aaa.is_root())
        self.assertEqual(aaa.get_ancestors_count(), 0)
        self.assertEqual(aaa.get_parent(), None)
        self.assertTrue(aaaa.is_root())
        self.assertEqual(aaaa.get_ancestors_count(), 0)
        self.assertEqual(aaaa.get_parent(), None)

    def test_get_priority(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(Category.get_roots(), [a, b, c, d, e, f])
        f.set_priority(60)
        e.set_priority(50)
        d.set_priority(40)
        c.set_priority(30)
        b.set_priority(20)
        a.set_priority(10)
        self.assertEqual(Category.get_roots(), [f, e, d, c, b, a])
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(a.get_children(), [aa, ab, ac, ad, ae, af])
        af.set_priority(60)
        ae.set_priority(50)
        ad.set_priority(40)
        ac.set_priority(30)
        ab.set_priority(20)
        aa.set_priority(10)
        self.assertEqual(a.get_children(), [af, ae, ad, ac, ab, aa])

    def test_get_root(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.get_root(), a)
        self.assertEqual(aa.get_root(), a)
        self.assertEqual(aaa.get_root(), a)
        self.assertEqual(aaaa.get_root(), a)

    def test_get_roots(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(Category.get_roots(), [a, b, c, d, e, f])

    def test_get_siblings(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.tn_siblings_pks, join_pks([b.pk, c.pk, d.pk, e.pk, f.pk]))
        self.assertEqual(b.tn_siblings_pks, join_pks([a.pk, c.pk, d.pk, e.pk, f.pk]))
        self.assertEqual(c.tn_siblings_pks, join_pks([a.pk, b.pk, d.pk, e.pk, f.pk]))
        self.assertEqual(d.tn_siblings_pks, join_pks([a.pk, b.pk, c.pk, e.pk, f.pk]))
        self.assertEqual(e.tn_siblings_pks, join_pks([a.pk, b.pk, c.pk, d.pk, f.pk]))
        self.assertEqual(f.tn_siblings_pks, join_pks([a.pk, b.pk, c.pk, d.pk, e.pk]))
        self.assertEqual(a.get_siblings(), [b, c, d, e, f])
        self.assertEqual(b.get_siblings(), [a, c, d, e, f])
        self.assertEqual(c.get_siblings(), [a, b, d, e, f])
        self.assertEqual(d.get_siblings(), [a, b, c, e, f])
        self.assertEqual(e.get_siblings(), [a, b, c, d, f])
        self.assertEqual(f.get_siblings(), [a, b, c, d, e])
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(aa.tn_siblings_pks, join_pks([ab.pk, ac.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(ab.tn_siblings_pks, join_pks([aa.pk, ac.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(ac.tn_siblings_pks, join_pks([aa.pk, ab.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(ad.tn_siblings_pks, join_pks([aa.pk, ab.pk, ac.pk, ae.pk, af.pk]))
        self.assertEqual(ae.tn_siblings_pks, join_pks([aa.pk, ab.pk, ac.pk, ad.pk, af.pk]))
        self.assertEqual(af.tn_siblings_pks, join_pks([aa.pk, ab.pk, ac.pk, ad.pk, ae.pk]))
        self.assertEqual(aa.get_siblings(), [ab, ac, ad, ae, af])
        self.assertEqual(ab.get_siblings(), [aa, ac, ad, ae, af])
        self.assertEqual(ac.get_siblings(), [aa, ab, ad, ae, af])
        self.assertEqual(ad.get_siblings(), [aa, ab, ac, ae, af])
        self.assertEqual(ae.get_siblings(), [aa, ab, ac, ad, af])
        self.assertEqual(af.get_siblings(), [aa, ab, ac, ad, ae])

    def test_get_siblings_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.get_siblings_count(), 5)
        self.assertEqual(b.get_siblings_count(), 5)
        self.assertEqual(c.get_siblings_count(), 5)
        self.assertEqual(d.get_siblings_count(), 5)
        self.assertEqual(e.get_siblings_count(), 5)
        self.assertEqual(f.get_siblings_count(), 5)
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(aa.get_siblings_count(), 5)
        self.assertEqual(ab.get_siblings_count(), 5)
        self.assertEqual(ac.get_siblings_count(), 5)
        self.assertEqual(ad.get_siblings_count(), 5)
        self.assertEqual(ae.get_siblings_count(), 5)
        self.assertEqual(af.get_siblings_count(), 5)

    def test_get_tree(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        aca = self.__get_cat(name='aca')
        acaa = self.__get_cat(name='acaa')
        acab = self.__get_cat(name='acab')
        acb = self.__get_cat(name='acb')
        acc = self.__get_cat(name='acc')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        b = self.__get_cat(name='b')
        ba = self.__get_cat(name='ba')
        bb = self.__get_cat(name='bb')
        bc = self.__get_cat(name='bc')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        tree = [
            {
                'node': a,
                'tree': [
                    {
                        'node': aa,
                        'tree': [
                            {
                                'node': aaa,
                                'tree': [
                                    {
                                        'node': aaaa,
                                        'tree': [],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        'node': ab,
                        'tree': [],
                    },
                    {
                        'node': ac,
                        'tree': [
                            {
                                'node': aca,
                                'tree': [
                                    {
                                        'node': acaa,
                                        'tree': [],
                                    },
                                    {
                                        'node': acab,
                                        'tree': [],
                                    },
                                ],
                            },
                            {
                                'node': acb,
                                'tree': [],
                            },
                            {
                                'node': acc,
                                'tree': [],
                            },
                        ],
                    },
                    {
                        'node': ad,
                        'tree': [],
                    },
                    {
                        'node': ae,
                        'tree': [],
                    },
                    {
                        'node': af,
                        'tree': [],
                    },
                ],
            },
            {
                'node': b,
                'tree': [
                    {
                        'node': ba,
                        'tree': [],
                    },
                    {
                        'node': bb,
                        'tree': [],
                    },
                    {
                        'node': bc,
                        'tree': [],
                    },
                ],
            },
            {
                'node': c,
                'tree': [],
            },
            {
                'node': d,
                'tree': [],
            },
            {
                'node': e,
                'tree': [],
            },
            {
                'node': f,
                'tree': [],
            },
        ]
        self.assertEqual(tree, Category.get_tree())

    def test_get_tree_display(self):
        # TODO
        pass

    def test_is_first_child(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertTrue(a.is_first_child())
        self.assertFalse(b.is_first_child())
        self.assertFalse(c.is_first_child())
        self.assertFalse(d.is_first_child())
        self.assertFalse(e.is_first_child())
        self.assertFalse(f.is_first_child())
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertTrue(aa.is_first_child())
        self.assertFalse(ab.is_first_child())
        self.assertFalse(ac.is_first_child())
        self.assertFalse(ad.is_first_child())
        self.assertFalse(ae.is_first_child())
        self.assertFalse(af.is_first_child())

    def test_is_last_child(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertFalse(a.is_last_child())
        self.assertFalse(b.is_last_child())
        self.assertFalse(c.is_last_child())
        self.assertFalse(d.is_last_child())
        self.assertFalse(e.is_last_child())
        self.assertTrue(f.is_last_child())
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertFalse(aa.is_last_child())
        self.assertFalse(ab.is_last_child())
        self.assertFalse(ac.is_last_child())
        self.assertFalse(ad.is_last_child())
        self.assertFalse(ae.is_last_child())
        self.assertTrue(af.is_last_child())

    def test_properties(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        for obj in [a, aa, aaa, aaaa]:
            self.assertEqual(obj.get_ancestors(), obj.ancestors)
            self.assertEqual(obj.get_ancestors_count(), obj.ancestors_count)
            self.assertEqual(obj.get_children(), obj.children)
            self.assertEqual(obj.get_children_count(), obj.children_count)
            self.assertEqual(obj.get_depth(), obj.depth)
            self.assertEqual(obj.get_descendants(), obj.descendants)
            self.assertEqual(obj.get_descendants_count(), obj.descendants_count)
            self.assertEqual(obj.get_descendants_tree(), obj.descendants_tree)
            self.assertEqual(obj.get_descendants_tree_display(), obj.descendants_tree_display)
            self.assertEqual(obj.get_index(), obj.index)
            self.assertEqual(obj.get_level(), obj.level)
            self.assertEqual(obj.get_order(), obj.order)
            self.assertEqual(obj.get_parent(), obj.parent)
            self.assertEqual(obj.get_roots(), obj.roots)
            self.assertEqual(obj.get_root(), obj.root)
            self.assertEqual(obj.get_siblings(), obj.siblings)
            self.assertEqual(obj.get_siblings_count(), obj.siblings_count)
            self.assertEqual(obj.get_tree(), obj.tree)
            self.assertEqual(obj.get_tree_display(), obj.tree_display)

    def test_update_on_create(self):
        a = self.__create_cat(name='a')
        self.assertEqual(a.tn_children_pks, '')
        self.assertEqual(a.tn_ancestors_pks, '')
        self.assertEqual(a.tn_siblings_pks, '')
        self.assertEqual(a.tn_depth, 0)
        self.assertEqual(a.tn_index, 0)
        self.assertEqual(a.tn_level, 1)
        b = self.__create_cat(name='b')
        c = self.__create_cat(name='c')
        self.assertEqual(a.tn_children_pks, '')
        self.assertEqual(a.tn_ancestors_pks, '')
        self.assertEqual(a.tn_siblings_pks, join_pks([b.pk, c.pk]))
        aa = self.__create_cat(name='aa', parent=a)
        ab = self.__create_cat(name='ab', parent=a)
        ac = self.__create_cat(name='ac', parent=a)
        self.assertEqual(a.tn_children_pks, join_pks([aa.pk, ab.pk, ac.pk]))
        self.assertEqual(a.tn_depth, 1)

    def test_update_on_delete(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        Category.objects.filter(name='aa').delete()
        self.assertEqual(a.tn_children_pks, join_pks([ab.pk, ac.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(a.tn_children_count, 5)
        self.assertTrue(ab.is_first_child())
        Category.objects.filter(name='ab').delete()
        self.assertEqual(a.tn_children_pks, join_pks([ac.pk, ad.pk, ae.pk, af.pk]))
        self.assertEqual(a.tn_children_count, 4)
        self.assertTrue(ac.is_first_child())
        Category.objects.filter(name='ac').delete()
        self.assertEqual(a.tn_children_pks, join_pks([ad.pk, ae.pk, af.pk]))
        self.assertEqual(a.tn_children_count, 3)
        self.assertTrue(ad.is_first_child())
        Category.objects.filter(name='ad').delete()
        self.assertEqual(a.tn_children_pks, join_pks([ae.pk, af.pk]))
        self.assertEqual(a.tn_children_count, 2)
        self.assertTrue(ae.is_first_child())
        Category.objects.filter(name='ae').delete()
        self.assertEqual(a.tn_children_pks, join_pks([af.pk]))
        self.assertEqual(a.tn_children_count, 1)
        self.assertTrue(af.is_first_child())
        Category.objects.filter(name='af').delete()
        self.assertEqual(a.tn_children_pks, join_pks([]))
        self.assertEqual(a.tn_children_count, 0)
        Category.objects.filter(name='a').delete()
        Category.objects.filter(name='b').delete()
        Category.objects.filter(name='c').delete()
        with self.assertRaises(Category.DoesNotExist):
            a = self.__get_cat(name='a')
        with self.assertRaises(Category.DoesNotExist):
            aa = self.__get_cat(name='aa')
        with self.assertRaises(Category.DoesNotExist):
            aaa = self.__get_cat(name='aaa')
        with self.assertRaises(Category.DoesNotExist):
            aaa = self.__get_cat(name='aaaa')
        with self.assertRaises(Category.DoesNotExist):
            b = self.__get_cat(name='b')
        with self.assertRaises(Category.DoesNotExist):
            c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        self.assertTrue(d.is_first_child())
        self.assertEqual(d.get_siblings_count(), 2)

    def test_update_on_get(self):
        self.__create_cat(name='a')
        a = self.__get_cat(name='a')
        self.assertEqual(a.get_level(), 1)
        self.assertEqual(a.get_depth(), 0)

    def test_update_on_save(self):
        a = Category(name='a')
        a.save()
        self.assertEqual(a.get_level(), 1)
        self.assertEqual(a.get_depth(), 0)
