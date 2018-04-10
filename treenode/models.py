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
            return self.get_str(self.name)
    """

    SEPARATOR = '|'

    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE,
        blank=True, null=True)

    parents_pks = models.CharField(
        max_length=500, blank=True, default='', editable=False)
    parents_count = models.PositiveSmallIntegerField(default=0, editable=False)

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

    def get_parents(self):
        return list(self.__str_to_qs(self.parents_pks))

    def get_parents_pks(self):
        return self.__str_to_list(self.parents_pks)

    def get_parents_count(self):
        return self.parents_count

    def get_children(self):
        return list(self.__str_to_qs(self.children_pks))

    def get_children_pks(self):
        return self.__str_to_list(self.children_pks)

    def get_children_count(self):
        return self.children_count

    def get_children_tree(self):
        # TODO
        # tree = get_children_tree_pks()
        # pks = tree to flat dict
        # objs = query all objects by pks (or simply query all objects)
        # iterate over the tree and replace data with models
        raise NotImplementedError

    def get_children_tree_pks(self):
        if self.children_tree_pks:
            return json.loads(self.children_tree_pks)
        else:
            return []

    def get_siblings(self):
        return list(self.__str_to_qs(self.siblings_pks))

    def get_siblings_pks(self):
        return self.__str_to_list(self.siblings_pks)

    def get_siblings_count(self):
        return self.siblings_count

    def get_level(self):
        return self.level

    def get_depth(self):
        return self.depth

    def get_priority(self):
        return self.priority

    def get_str(self, text):
        t = self.get_parents_count()
        s = ('— ' * t)
        return force_text(s + text)

    def __list_to_str(self, l):
        s = TreeNodeModel.SEPARATOR.join([str(v) for v in l])
        return s

    def __str_to_list(self, s):
        l = [int(v) for v in s.split(TreeNodeModel.SEPARATOR) if v]
        return l

    def __str_to_qs(self, s):
        pks = self.__str_to_list(s)
        qs = self.__class__.objects.filter(pk__in=pks).order_by('order')
        return qs

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

        data = {}

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
        data['parents_pks'] = self.__list_to_str(parents_pks)
        data['parents_count'] = parents_count

        # update children
        children_list = list(objs_manager.filter(
            parent=self.pk).values_list('pk', flat=True))

        data['children_pks'] = self.__list_to_str(children_list)
        data['children_count'] = len(children_list)

        # update siblings
        siblings_list = list(objs_manager.filter(
            parent=parent_obj).exclude(
            pk=self.pk).values_list('pk', flat=True))

        data['siblings_pks'] = self.__list_to_str(siblings_list)
        data['siblings_count'] = len(siblings_list)

        # update level
        data['level'] = parents_count + 1

        # update depth
        data['depth'] = 0

        # update order
        order_objs = list(parents_list) + [self]
        order_strs = [obj.__get_node_order_str() for obj in order_objs]
        order_str = ''.join(order_strs)[0:150]
        data['order'] = order_str

        return data

    @staticmethod
    @receiver(post_delete, dispatch_uid='post_delete_treenode')
    @receiver(post_save, dispatch_uid='post_save_treenode')
    def __update_nodes_data(sender, instance, **kwargs):

        if not isinstance(instance, TreeNodeModel):
            return

        if settings.DEBUG:
            import timeit
            start_time = timeit.default_timer()

        objs_manager = sender.objects
        objs_filter = objs_manager.filter
        objs_qs = objs_manager.select_related(
            'parent').prefetch_related('children')
        objs_list = list(objs_qs)
        objs_dict = {}
        objs_tree = []

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
            obj_parents_keys = obj_data['parents_pks'].split(
                TreeNodeModel.SEPARATOR)
            for obj_parent_key in obj_parents_keys:
                obj_parent_data = objs_dict[obj_parent_key]
                obj_parent_index = obj_parents_keys.index(obj_parent_key)
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
            obj_children_keys = obj_data['children_pks'].split(
                TreeNodeModel.SEPARATOR)
            for obj_child_key in obj_children_keys:
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

        # print(json.dumps(objs_dict, indent=4))
        # print(json.dumps(objs_tree, indent=4))

        # update db data
        for obj_key in objs_dict:
            obj_pk = int(obj_key)
            obj_data = objs_dict[obj_key]
            objs_filter(pk=obj_pk).update(**obj_data)

        if settings.DEBUG:
            elapsed = timeit.default_timer() - start_time
            print('%s.__update_nodes_data in %ss' %
                  (instance.__class__.__name__, elapsed, ))

    class Meta:
        abstract = True
        ordering = ['order']
