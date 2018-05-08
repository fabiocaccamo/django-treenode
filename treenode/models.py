# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from . import classproperty
# from .debug import debug_performance
from .memory import clear_refs, get_refs
from .signals import connect_signals, no_signals
from .utils import join_pks, split_pks


@python_2_unicode_compatible
class TreeNodeModel(models.Model):

    """
    Usage:

    from django.db import models
    from treenode.models import TreeNodeModel


    class MyModel(TreeNodeModel):

        treenode_display_field = 'name'

        name = models.CharField(max_length=50)

        class Meta(TreeNodeModel.Meta):
            verbose_name = 'My Model'
            verbose_name_plural = 'My Models'
    """

    # Options
    treenode_display_field = None

    # Fields
    # All fields are for internal usage and they are prefixed by 'tn_'
    # to avoid direct access and conflicts with possible existing fields.

    tn_ancestors_pks = models.CharField(
        max_length=500, blank=True,
        default='', editable=False,
        verbose_name=_('Ancestors pks'), )

    tn_ancestors_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Ancestors count'), )

    tn_children_pks = models.CharField(
        max_length=500, blank=True,
        default='', editable=False,
        verbose_name=_('Children pks'), )

    tn_children_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Children count'), )

    tn_depth = models.PositiveSmallIntegerField(
        default=0, editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('Depth'), )

    tn_descendants_pks = models.CharField(
        max_length=500, blank=True,
        default='', editable=False,
        verbose_name=_('Descendants pks'), )

    tn_descendants_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Descendants count'), )

    tn_index = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Index'), )

    tn_level = models.PositiveSmallIntegerField(
        default=0, editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('Level'), )

    tn_parent = models.ForeignKey('self',
        related_name='tn_children',
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_('Parent'), )

    tn_priority = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_('Priority'), )

    tn_order = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Order'), )

    tn_siblings_pks = models.CharField(
        max_length=500, blank=True,
        default='', editable=False,
        verbose_name=_('Siblings pks'), )

    tn_siblings_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Siblings count'), )

    # Public methods

    def delete(self):
        with no_signals():
            self.__class__.objects.filter(pk=self.pk).delete()
        self.update_tree()

    @classmethod
    def delete_tree(cls):
        with no_signals():
            with transaction.atomic():
                cls.objects.all().delete()
            clear_refs(cls)

    def get_ancestors(self):
        return list(self.get_ancestors_queryset())

    def get_ancestors_count(self):
        return self.tn_ancestors_count

    def get_ancestors_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_ancestors_pks))

    def get_children(self):
        return list(self.get_children_queryset())

    def get_children_count(self):
        return self.tn_children_count

    def get_children_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_children_pks))

    def get_depth(self):
        return self.tn_depth

    def get_descendants(self):
        return list(self.get_descendants_queryset())

    def get_descendants_count(self):
        return self.tn_descendants_count

    def get_descendants_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_descendants_pks))

    def get_descendants_tree(self):
        return self.__get_nodes_tree(self)

    def get_descendants_tree_display(self):
        objs = list(self.get_descendants_queryset())
        strs = ['%s' % (obj, ) for obj in objs]
        d = '\n'.join(strs)
        return d

    # def get_descendants_tree_dump(self, indent=2, default=None):
    #     data = self.get_descendants_tree()
    #     func = lambda obj:str(obj.pk)
    #     dump = json.dumps(data,
    #         sort_keys=True,
    #         indent=indent,
    #         default=func if not default else default)
    #     return dump

    def get_display(self, indent=True, mark='— '):
        indentation = '%s' % ((mark * self.tn_ancestors_count) if indent else '', )
        field_name = getattr(self, 'treenode_display_field', 'pk')
        text = str(getattr(self, field_name))
        return force_text(indentation + text)

    def get_index(self):
        return self.tn_index

    def get_level(self):
        return self.tn_level

    def get_order(self):
        return self.tn_order

    def get_parent(self):
        return self.tn_parent

    def set_parent(self, obj):
        with no_signals():
            if obj:
                obj_cls = obj.__class__
                cls = self.__class__
                if obj_cls != cls:
                    raise ValueError(
                        'obj can\'t be set as parent, '\
                        'it is istance of %s, expected instance of %s.' % (
                        obj_cls.__name__, cls.__name__, ))
                if obj == self:
                    raise ValueError(
                        'obj can\'t be set as parent of itself.')
                if not obj.pk:
                    obj.save()
                if obj.pk in split_pks(self.tn_descendants_pks):
                    obj.tn_parent = self.tn_parent
                    obj.save()
            self.tn_parent = obj
            self.save()
        self.update_tree()

    def get_priority(self):
        return self.tn_priority

    def set_priority(self, val):
        self.tn_priority = val
        self.save()

    def get_root(self):
        root_pk = (split_pks(self.tn_ancestors_pks) + [self.pk])[0]
        root_obj = self.__class__.objects.get(pk=root_pk)
        return root_obj

    @classmethod
    def get_roots(cls):
        return list(cls.get_roots_queryset())

    @classmethod
    def get_roots_queryset(cls):
        return cls.objects.filter(tn_parent=None)

    def get_siblings(self):
        return list(self.get_siblings_queryset())

    def get_siblings_count(self):
        return self.tn_siblings_count

    def get_siblings_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_siblings_pks))

    @classmethod
    def get_tree(cls):
        return cls.__get_nodes_tree()

    @classmethod
    def get_tree_display(cls):
        objs = list(cls.objects.all())
        strs = ['%s' % (obj, ) for obj in objs]
        d = '\n'.join(strs)
        return d

    # @classmethod
    # def get_tree_dump(cls, indent=2, default=None):
    #     data = cls.get_tree()
    #     func = lambda obj:str(obj.pk)
    #     dump = json.dumps(data,
    #         sort_keys=True,
    #         indent=indent,
    #         default=func if not default else default)
    #     return dump

    def is_ancestor_of(self, obj):
        return (self.__class__ == obj.__class__ and \
                self.pk and \
                self.pk != obj.pk and \
                self.pk in split_pks(obj.tn_ancestors_pks))

    def is_child_of(self, obj):
        return (self.__class__ == obj.__class__ and \
                self.pk and \
                self.pk != obj.pk and \
                self.pk in split_pks(obj.tn_children_pks))

    def is_descendant_of(self, obj):
        return (self.__class__ == obj.__class__ and \
                self.pk and \
                self.pk != obj.pk and \
                self.pk in split_pks(obj.tn_descendants_pks))

    def is_first_child(self):
        return (self.pk and \
                self.tn_index == 0)

    def is_last_child(self):
        return (self.pk and \
                self.tn_index == self.tn_siblings_count)

    def is_leaf(self):
        return (self.pk and \
                self.tn_children_count == 0)

    def is_parent_of(self, obj):
        return (self.__class__ == obj.__class__ and \
                self.pk and \
                self.pk != obj.pk and \
                obj.tn_ancestors_count > 0 and \
                self.pk == split_pks(obj.tn_ancestors_pks)[-1])

    def is_root(self):
        return (self.pk and \
                self.tn_ancestors_count == 0)

    def is_root_of(self, obj):
        return (self.is_root() and self.is_ancestor_of(obj))

    def is_sibling_of(self, obj):
        return (self.__class__ == obj.__class__ and \
                self.pk and \
                self.pk != obj.pk and \
                self.tn_ancestors_pks == obj.tn_ancestors_pks)

    @classmethod
    def update_tree(cls):

        # with debug_performance(cls):

        # update db
        objs_list, objs_dict = cls.__get_nodes_data()
        with transaction.atomic():
            for obj_key, obj_data in objs_dict.items():
                obj_pk = int(obj_key)
                cls.objects.filter(pk=obj_pk).update(**obj_data)

        # update in-memory instances
        for obj in get_refs(cls):
            obj_data = objs_dict.get(str(obj.pk))
            if obj_data:
                obj.__update_node_data(obj_data)

    # Private methods

    def __get_node_order_str(self):
        priority_max = 99999
        priority_len = len(str(priority_max))
        priority_val = priority_max - min(self.tn_priority, priority_max)
        priority_key = str(priority_val).zfill(priority_len)
        alphabetical_val = slugify(str(self))
        alphabetical_key = alphabetical_val.rjust(priority_len, str('z'))
        alphabetical_key = alphabetical_key[0:priority_len]
        pk_val = min(self.pk, priority_max)
        pk_key = str(pk_val).zfill(priority_len)
        s = '%s%s%s' % (priority_key, alphabetical_key, pk_key, )
        s = s.upper()
        return s

    def __get_node_data(self, objs):

        obj_dict = {}

        # update ancestors
        ancestors_list = []

        parent_obj = self.tn_parent
        while parent_obj:
            ancestors_list.insert(0, parent_obj)
            parent_obj = parent_obj.tn_parent

        ancestors_pks = [obj.pk for obj in ancestors_list]
        ancestors_count = len(ancestors_pks)

        obj_dict['tn_ancestors_pks'] = ancestors_pks
        obj_dict['tn_ancestors_count'] = ancestors_count

        # update children
        children_pks = [
            obj.pk for obj in objs \
            if obj.tn_parent == self]
        children_count = len(children_pks)

        obj_dict['tn_children_pks'] = children_pks
        obj_dict['tn_children_count'] = children_count

        # update depth
        obj_dict['tn_depth'] = 0

        # update descendants
        obj_dict['tn_descendants_pks'] = []
        obj_dict['tn_descendants_count'] = 0

        # update level
        obj_dict['tn_level'] = (ancestors_count + 1)

        # update order
        order_objs = list(ancestors_list) + [self]
        order_strs = [obj.__get_node_order_str() for obj in order_objs]
        order_str = ''.join(order_strs)[0:150]
        obj_dict['tn_order_str'] = order_str

        # update siblings
        siblings_pks = [
            obj.pk for obj in objs \
            if obj.tn_parent == self.tn_parent and obj.pk != self.pk]
        siblings_count = len(siblings_pks)

        obj_dict['tn_siblings_pks'] = siblings_pks
        obj_dict['tn_siblings_count'] = siblings_count

        return obj_dict

    @classmethod
    def __get_nodes_data(cls):

        objs_qs = cls.objects.select_related('tn_parent').select_for_update()
        objs_list = list(objs_qs)
        objs_dict = {
            str(obj.pk):obj.__get_node_data(objs_list) \
            for obj in objs_list}

        # get sorted dict keys
        objs_dict_keys = list(objs_dict.keys())
        objs_dict_keys.sort(
            key=lambda obj_key: objs_dict[obj_key]['tn_order_str'])

        # get sorted dict values
        objs_dict_values = list(objs_dict.values())
        objs_dict_values.sort(
            key=lambda obj_value: obj_value['tn_order_str'])

        objs_sort_pks = lambda obj_pk: objs_dict_keys.index(str(obj_pk))

        # update order
        objs_order_cursor = 0
        for obj_data in objs_dict_values:
            obj_data.pop('tn_order_str', None)
            obj_data['tn_order'] = objs_order_cursor
            objs_order_cursor += 1

        # update index
        objs_index_cursors = {}
        objs_index_cursor = 0
        for obj_data in objs_dict_values:
            obj_ancestors_pks = str(obj_data['tn_ancestors_pks'])
            objs_index_cursor = objs_index_cursors.get(obj_ancestors_pks, 0)
            obj_data['tn_index'] = objs_index_cursor
            objs_index_cursor += 1
            objs_index_cursors[obj_ancestors_pks] = objs_index_cursor

        # update depth
        for obj_data in objs_dict_values:
            obj_children_count = obj_data['tn_children_count']
            if obj_children_count > 0:
                continue
            obj_ancestors_count = obj_data['tn_ancestors_count']
            if obj_ancestors_count == 0:
                continue
            obj_ancestors_pks = obj_data['tn_ancestors_pks']
            for obj_ancestor_pk in obj_ancestors_pks:
                obj_ancestor_key = str(obj_ancestor_pk)
                obj_ancestor_data = objs_dict[obj_ancestor_key]
                obj_ancestor_index = obj_ancestors_pks.index(obj_ancestor_pk)
                obj_ancestor_depth = (obj_ancestors_count - obj_ancestor_index)
                if obj_ancestor_data['tn_depth'] < obj_ancestor_depth:
                    obj_ancestor_data['tn_depth'] = obj_ancestor_depth

        # update children and siblings pks order
        for obj_data in objs_dict_values:
            # update children pks order
            if obj_data['tn_children_pks']:
                obj_data['tn_children_pks'].sort(key=objs_sort_pks)
            # update siblings pks order
            if obj_data['tn_siblings_pks']:
                obj_data['tn_siblings_pks'].sort(key=objs_sort_pks)

        # update descendants pks
        objs_dict_values.sort(key=lambda obj: obj['tn_level'], reverse=True)
        for obj_data in objs_dict_values:
            if obj_data['tn_children_count'] == 0:
                continue
            obj_children_pks = obj_data['tn_children_pks']
            obj_descendants_pks = list(obj_children_pks)
            for obj_child_pk in obj_children_pks:
                obj_child_key = str(obj_child_pk)
                obj_child_data = objs_dict[obj_child_key]
                obj_child_descendants_pks = obj_child_data.get('tn_descendants_pks', [])
                if obj_child_descendants_pks:
                    obj_descendants_pks += obj_child_descendants_pks
            obj_data['tn_descendants_pks'] = obj_descendants_pks
            # update descendants pks order
            if obj_data['tn_descendants_pks']:
                obj_data['tn_descendants_pks'].sort(key=objs_sort_pks)
                obj_data['tn_descendants_count'] = len(obj_data['tn_descendants_pks'])

        # join all pks lists
        for obj_data in objs_dict_values:
            obj_data['tn_ancestors_pks'] = join_pks(obj_data['tn_ancestors_pks'])
            obj_data['tn_children_pks'] = join_pks(obj_data['tn_children_pks'])
            obj_data['tn_descendants_pks'] = join_pks(obj_data['tn_descendants_pks'])
            obj_data['tn_siblings_pks'] = join_pks(obj_data['tn_siblings_pks'])

        # clean dict data
        for obj in objs_list:
            obj_key = str(obj.pk)
            obj_data = objs_dict[obj_key]

            if obj_data['tn_ancestors_count'] == obj.tn_ancestors_count:
                obj_data.pop('tn_ancestors_count')

            if obj_data['tn_ancestors_pks'] == obj.tn_ancestors_pks:
                obj_data.pop('tn_ancestors_pks', None)

            if obj_data['tn_children_count'] == obj.tn_children_count:
                obj_data.pop('tn_children_count', None)

            if obj_data['tn_children_pks'] == obj.tn_children_pks:
                obj_data.pop('tn_children_pks', None)

            if obj_data['tn_depth'] == obj.tn_depth:
                obj_data.pop('tn_depth', None)

            if obj_data['tn_descendants_count'] == obj.tn_descendants_count:
                obj_data.pop('tn_descendants_count', None)

            if obj_data['tn_descendants_pks'] == obj.tn_descendants_pks:
                obj_data.pop('tn_descendants_pks', None)

            if obj_data['tn_index'] == obj.tn_index:
                obj_data.pop('tn_index', None)

            if obj_data['tn_level'] == obj.tn_level:
                obj_data.pop('tn_level', None)

            if obj_data['tn_order'] == obj.tn_order:
                obj_data.pop('tn_order', None)

            if obj_data['tn_siblings_count'] == obj.tn_siblings_count:
                obj_data.pop('tn_siblings_count', None)

            if obj_data['tn_siblings_pks'] == obj.tn_siblings_pks:
                obj_data.pop('tn_siblings_pks', None)

            if len(obj_data) == 0:
                objs_dict.pop(obj_key, None)

        # clean list data
        objs_list = [obj for obj in objs_list if str(obj.pk) in objs_dict]

        return (objs_list, objs_dict, )

    @classmethod
    def __get_nodes_tree(cls, instance=None):

        def __get_node_tree(obj):
            child_tree = { 'node':obj, 'tree':[] }
            if obj.tn_children_pks:
                children_pks = split_pks(obj.tn_children_pks)
                for child_pk in children_pks:
                    child_key = str(child_pk)
                    child_obj = objs_dict.get(child_key)
                    if child_obj:
                        child_tree['tree'].append(
                            __get_node_tree(child_obj))
            return child_tree

        if instance:
            objs_pks = split_pks(instance.tn_descendants_pks)
            objs_list = list(cls.objects.filter(pk__in=objs_pks))
            objs_dict = { str(obj.pk):obj for obj in objs_list }
            objs_tree = __get_node_tree(instance)['tree']
        else:
            objs_list = list(cls.objects.all())
            objs_dict = { str(obj.pk):obj for obj in objs_list }
            objs_tree = [__get_node_tree(obj) for obj in objs_list if obj.tn_level == 1]

        return objs_tree

    def __update_node_data(self, data):
        if data:
            for key, value in data.items():
                setattr(self, key, value)

    class Meta:
        abstract = True
        ordering = ['tn_order']

    def __str__(self):
        return self.get_display(indent=True)


class TreeNodeProperties(object):

    """
    Public properties
    All properties map a get_{{property}}() method.
    """

    @property
    def ancestors(self):
        return self.get_ancestors()

    @property
    def ancestors_count(self):
        return self.get_ancestors_count()

    @property
    def children(self):
        return self.get_children()

    @property
    def children_count(self):
        return self.get_children_count()

    @property
    def depth(self):
        return self.get_depth()

    @property
    def descendants(self):
        return self.get_descendants()

    @property
    def descendants_count(self):
        return self.get_descendants_count()

    @property
    def descendants_tree(self):
        return self.get_descendants_tree()

    @property
    def descendants_tree_display(self):
        return self.get_descendants_tree_display()

    @property
    def index(self):
        return self.get_index()

    @property
    def level(self):
        return self.get_level()

    @property
    def order(self):
        return self.get_order()

    @property
    def parent(self):
        return self.get_parent()

    @property
    def priority(self):
        return self.get_priority()

    @classproperty
    def roots(cls):
        return cls.get_roots()

    @property
    def root(self):
        return self.get_root()

    @property
    def siblings(self):
        return self.get_siblings()

    @property
    def siblings_count(self):
        return self.get_siblings_count()

    @classproperty
    def tree(cls):
        return cls.get_tree()

    @classproperty
    def tree_display(cls):
        return cls.get_tree_display()


connect_signals()
