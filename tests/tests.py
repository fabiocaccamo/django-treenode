# -*- coding: utf-8 -*-

from django.test import TestCase

from .models import Category


class TreeNodeTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def __create_cat(self, name, parent=None):
        return Category.objects.create(name=name, tn_parent=parent)

    def __create_cat_tree(self):
        """
            a
                aa
                    aaa
                        aaaa
                ab
                ac
                    aca
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

    def test_update_on_save(self):
        a = Category(name='a')
        a.save()
        self.assertEqual(a.level, 1)
        self.assertEqual(a.depth, 0)

    def test_update_on_create(self):
        a = self.__create_cat(name='a')
        self.assertEqual(a.level, 1)
        self.assertEqual(a.depth, 0)

    def test_update_on_get(self):
        self.__create_cat(name='a')
        a = self.__get_cat(name='a')
        self.assertEqual(a.level, 1)
        self.assertEqual(a.depth, 0)

    def test_update_on_delete(self):
        self.__create_cat_tree()

    def test_tree(self):
        pass

    def test_roots(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(Category.roots, [a, b, c, d, e, f])

    def test_root(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.root, a)
        self.assertEqual(aa.root, a)
        self.assertEqual(aaa.root, a)
        self.assertEqual(aaaa.root, a)

    def test_parent(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        self.assertEqual(a, aa.parent)

    def test_parents_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.parents_count, 0)
        self.assertEqual(aa.parents_count, 1)
        self.assertEqual(aaa.parents_count, 2)
        self.assertEqual(aaaa.parents_count, 3)

    def test_parents(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(aaaa.parents, [a, aa, aaa])

    def test_children_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        self.assertEqual(a.children_count, 6)

    def test_children(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        ab = self.__get_cat(name='ab')
        ac = self.__get_cat(name='ac')
        ad = self.__get_cat(name='ad')
        ae = self.__get_cat(name='ae')
        af = self.__get_cat(name='af')
        self.assertEqual(a.children, [aa, ab, ac, ad, ae, af])

    def test_children_tree(self):
        pass

    def test_siblings_count(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.siblings_count, 5)
        self.assertEqual(b.siblings_count, 5)
        self.assertEqual(c.siblings_count, 5)
        self.assertEqual(d.siblings_count, 5)
        self.assertEqual(e.siblings_count, 5)
        self.assertEqual(f.siblings_count, 5)

    def test_siblings(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        b = self.__get_cat(name='b')
        c = self.__get_cat(name='c')
        d = self.__get_cat(name='d')
        e = self.__get_cat(name='e')
        f = self.__get_cat(name='f')
        self.assertEqual(a.siblings, [b, c, d, e, f])
        self.assertEqual(b.siblings, [a, c, d, e, f])
        self.assertEqual(c.siblings, [a, b, d, e, f])
        self.assertEqual(d.siblings, [a, b, c, e, f])
        self.assertEqual(e.siblings, [a, b, c, d, f])
        self.assertEqual(f.siblings, [a, b, c, d, e])

    def test_level(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.level, 1)
        self.assertEqual(aa.level, 2)
        self.assertEqual(aaa.level, 3)
        self.assertEqual(aaaa.level, 4)

    def test_index(self):
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
        self.assertEqual(a.index, 0)
        self.assertEqual(aa.index, 0)
        self.assertEqual(aaa.index, 0)
        self.assertEqual(aaaa.index, 0)
        self.assertEqual(ab.index, 1)
        self.assertEqual(ac.index, 2)
        self.assertEqual(ad.index, 3)
        self.assertEqual(ae.index, 4)
        self.assertEqual(af.index, 5)
        self.assertEqual(b.index, 1)
        self.assertEqual(c.index, 2)
        self.assertEqual(d.index, 3)
        self.assertEqual(e.index, 4)
        self.assertEqual(f.index, 5)

    def test_depth(self):
        self.__create_cat_tree()
        a = self.__get_cat(name='a')
        aa = self.__get_cat(name='aa')
        aaa = self.__get_cat(name='aaa')
        aaaa = self.__get_cat(name='aaaa')
        self.assertEqual(a.depth, 3)
        self.assertEqual(aa.depth, 2)
        self.assertEqual(aaa.depth, 1)
        self.assertEqual(aaaa.depth, 0)

    def test_priority(self):
        pass

    def test_order(self):
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
        self.assertEqual(a.order, 0)
        self.assertEqual(aa.order, 1)
        self.assertEqual(aaa.order, 2)
        self.assertEqual(aaaa.order, 3)
        self.assertEqual(ab.order, 4)
        self.assertEqual(ac.order, 5)
        self.assertEqual(aca.order, 6)
        self.assertEqual(acaa.order, 7)
        self.assertEqual(acab.order, 8)
        self.assertEqual(acb.order, 9)
        self.assertEqual(acc.order, 10)
        self.assertEqual(ad.order, 11)
        self.assertEqual(ae.order, 12)
        self.assertEqual(af.order, 13)
        self.assertEqual(b.order, 14)
        self.assertEqual(ba.order, 15)
        self.assertEqual(bb.order, 16)
        self.assertEqual(bc.order, 17)
        self.assertEqual(c.order, 18)
        self.assertEqual(d.order, 19)
        self.assertEqual(e.order, 20)
        self.assertEqual(f.order, 21)
