# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import slugify

import json


class classproperty(object):

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class TreeNodeModel(models.Model):

    """
    Usage:

    from __future__ import unicode_literals

    from django.db import models
    from django.utils.encoding import python_2_unicode_compatible

    from treenode.models import TreeNodeModel


    @python_2_unicode_compatible
    class MyModel(TreeNodeModel):

        name = models.CharField(max_length=50)

        class Meta(TreeNodeModel.Meta):
            verbose_name = 'My Model'
            verbose_name_plural = 'My Models'

        def __str__(self):
            return self.get_display(self.name)
    """

    PKS_SEPARATOR = '|'

    @classmethod
    def join_pks(cls, l):
        s = TreeNodeModel.PKS_SEPARATOR.join([str(v) for v in l])
        return s

    @classmethod
    def split_pks(cls, s):
        l = [int(v) for v in s.split(TreeNodeModel.PKS_SEPARATOR) if v]
        return l

    @classmethod
    def queryset_pks(cls, s):
        pks = cls.split_pks(s)
        qs = cls.objects.filter(pk__in=pks)
        return qs

    @classmethod
    def query_pks(cls, s):
        l = list(cls.queryset_pks(s))
        return l

    parent = models.ForeignKey(
        'self', related_name='children_set', on_delete=models.CASCADE,
        blank=True, null=True)

    parents_pks = models.CharField(
        max_length=500, blank=True, default='', editable=False)
    parents_count = models.PositiveSmallIntegerField(
        default=0, editable=False)

    children_pks = models.CharField(
        max_length=500, blank=True, default='', editable=False)
    children_count = models.PositiveSmallIntegerField(
        default=0, editable=False)
    children_tree_pks = models.TextField(
        blank=True, editable=False)

    siblings_pks = models.CharField(
        max_length=500, blank=True, default='', editable=False)
    siblings_count = models.PositiveSmallIntegerField(
        default=0, editable=False)

    level = models.PositiveSmallIntegerField(
        default=0, editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(9999)])

    depth = models.PositiveSmallIntegerField(
        default=0, editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    priority = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])

    order = models.CharField(
        max_length=150, blank=True, default='', editable=False)

    @classproperty
    def tree(cls):
        return cls.get_tree()

    @classproperty
    def roots(cls):
        return cls.get_roots()

    @property
    def root(self):
        return self.get_root()

    @property
    def parents(self):
        return self.get_parents()

    @property
    def children(self):
        return self.get_children()

    @property
    def children_tree(self):
        return self.get_children_tree()

    @property
    def siblings(self):
        return self.get_siblings()

    @classmethod
    def get_display(cls):
        objs = list(cls.objects.all())
        strs = [str(obj) for obj in objs]
        d = '\n'.join(strs)
        return d

    def get_display_text(self, text='', tab='— '):
        tabs = (tab * self.parents_count)
        text = text or str(self.pk)
        return force_text(tabs + text)

    @classmethod
    def get_tree(cls):
        roots = cls.get_roots()
        tree = [{str(obj.pk): obj.get_children_tree()} for obj in roots]
        return tree

    @classmethod
    def get_roots(cls):
        return list(cls.objects.filter(parent=None))

    def get_root(self):
        root_pk = (self.split_pks(self.parents_pks) + [self.pk])[0]
        root_obj = self.__class__.objects.get(pk=root_pk)
        return root_obj

    def get_parents(self):
        return self.query_pks(self.parents_pks)

    def get_children(self):
        return self.query_pks(self.children_pks)

    def get_children_tree(self):
        # TODO:
        # objs_tree = json.loads(self.children_tree_pks) if self.children_tree_pks else []
        # objs_pks = get all keys in objs_tree
        # objs_list = self.__class__.objects.filter(pk__in=objs_pks)
        # iterate objs_tree and decorate data with model instances
        raise NotImplementedError

    def get_siblings(self):
        return self.query_pks(self.siblings_pks)

    def __get_node_order_str(self):
        priority_max = 99999
        priority_len = len(str(priority_max))
        priority_val = priority_max - min(self.priority, priority_max)
        priority_key = str(priority_val).zfill(priority_len)
        alphabetical_val = slugify(str(self))
        alphabetical_key = alphabetical_val.rjust(priority_len, str('z'))
        alphabetical_key = alphabetical_key[0:priority_len]
        pk_val = min(self.pk, priority_max)
        pk_key = str(pk_val).zfill(priority_len)
        s = '%s%s%s' % (priority_key, alphabetical_key, pk_key, )
        s = s.upper()
        return s

    def __get_node_data(self):

        obj_dict = {}
        objs_manager = self.__class__.objects

        # retrieve parents
        parent_obj = self.parent
        parents_list = []
        obj = parent_obj

        while obj:
            parents_list.insert(0, obj)
            obj = obj.parent

        parents_pks = [obj.pk for obj in parents_list]
        parents_count = len(parents_list)

        # update parents
        obj_dict['parents_pks'] = self.join_pks(parents_pks)
        obj_dict['parents_count'] = parents_count

        # update children
        children_list = list(objs_manager.filter(
            parent=self.pk).values_list('pk', flat=True))

        obj_dict['children_pks'] = self.join_pks(children_list)
        obj_dict['children_count'] = len(children_list)

        # update siblings
        siblings_list = list(objs_manager.filter(
            parent=parent_obj).exclude(
            pk=self.pk).values_list('pk', flat=True))

        obj_dict['siblings_pks'] = self.join_pks(siblings_list)
        obj_dict['siblings_count'] = len(siblings_list)

        # update level
        obj_dict['level'] = parents_count + 1

        # update depth
        obj_dict['depth'] = 0

        # update order
        order_objs = list(parents_list) + [self]
        order_strs = [obj.__get_node_order_str() for obj in order_objs]
        order_str = ''.join(order_strs)[0:150]
        obj_dict['order'] = order_str

        return obj_dict

    @classmethod
    def __get_nodes_data(cls):

        objs_dict = {}
        objs_tree = []

        objs_qs = cls.objects.select_related(
            'parent').prefetch_related('children_set')
        objs_list = list(objs_qs)

        for obj in objs_list:
            obj_key = str(obj.pk)
            obj_data = obj.__get_node_data()
            objs_dict[obj_key] = obj_data

        # update depths
        for obj_key in objs_dict:
            obj_data = objs_dict[obj_key]
            obj_children_count = obj_data['children_count']
            if obj_children_count > 0:
                continue
            obj_parents_count = obj_data['parents_count']
            if obj_parents_count == 0:
                continue
            obj_parents_pks = cls.split_pks(obj_data['parents_pks'])
            for obj_parent_pk in obj_parents_pks:
                obj_parent_key = str(obj_parent_pk)
                obj_parent_data = objs_dict[obj_parent_key]
                obj_parent_index = obj_parents_pks.index(obj_parent_pk)
                obj_parent_depth = (obj_parents_count - obj_parent_index)
                if obj_parent_data['depth'] < obj_parent_depth:
                    obj_parent_data['depth'] = obj_parent_depth

        # update trees
        def __get_children_tree_data(obj_key):
            obj_data = objs_dict.get(obj_key)
            obj_tree_data = {obj_key: []}
            obj_children_count = obj_data['children_count']
            if obj_children_count == 0:
                return obj_tree_data
            obj_children_pks = cls.split_pks(obj_data['children_pks'])
            for obj_child_pk in obj_children_pks:
                obj_child_key = str(obj_child_pk)
                obj_child_tree = __get_children_tree_data(obj_child_key)
                obj_tree_data[obj_key].append(obj_child_tree)
            return obj_tree_data

        for obj_key in objs_dict:
            obj_data = objs_dict[obj_key]
            obj_parents_count = obj_data['parents_count']
            obj_children_tree_data = __get_children_tree_data(obj_key)
            obj_children_tree_pks = json.dumps(obj_children_tree_data[obj_key])
            obj_data['children_tree_pks'] = obj_children_tree_pks
            if obj_parents_count == 0:
                objs_tree.append(obj_children_tree_data)

        return (objs_dict, objs_tree, )

    @staticmethod
    @receiver(post_delete, dispatch_uid='post_delete_treenode')
    @receiver(post_save, dispatch_uid='post_save_treenode')
    def __update_nodes_data(sender, instance, **kwargs):

        if not isinstance(instance, TreeNodeModel):
            return

        if settings.DEBUG:
            import timeit
            start_time = timeit.default_timer()

        objs_dict, objs_tree = sender.__get_nodes_data()
        # print(json.dumps(objs_dict, indent=4))
        # print(json.dumps(objs_tree, indent=4))

        # update db data
        for obj_key in objs_dict:
            obj_pk = int(obj_key)
            obj_data = objs_dict[obj_key]
            sender.objects.filter(pk=obj_pk).update(**obj_data)

        # update instance data
        obj_key = str(instance.pk)
        obj_data = objs_dict[obj_key]
        for key, value in obj_data.items():
            setattr(instance, key, value)

        if settings.DEBUG:
            elapsed = timeit.default_timer() - start_time
            print('%s.__update_nodes_data in %ss' % (
                sender.__name__, elapsed, ))

    class Meta:
        abstract = True
        ordering = ['order']
