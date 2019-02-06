# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from . import classproperty
from .cache import clear_cache, query_cache, update_cache
from .debug import debug_performance
from .memory import clear_refs, update_refs
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

    tn_ancestors_pks = models.TextField(
        blank=True, default='', editable=False,
        verbose_name=_('Ancestors pks'), )

    tn_ancestors_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Ancestors count'), )

    tn_children_pks = models.TextField(
        blank=True, default='', editable=False,
        verbose_name=_('Children pks'), )

    tn_children_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Children count'), )

    tn_depth = models.PositiveSmallIntegerField(
        default=0, editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('Depth'), )

    tn_descendants_pks = models.TextField(
        blank=True, default='', editable=False,
        verbose_name=_('Descendants pks'), )

    tn_descendants_count = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Descendants count'), )

    tn_index = models.PositiveSmallIntegerField(
        default=0, editable=False,
        verbose_name=_('Index'), )

    tn_level = models.PositiveSmallIntegerField(
        default=1, editable=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
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

    tn_siblings_pks = models.TextField(
        blank=True, default='', editable=False,
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
            clear_cache(cls)

    def get_ancestors(self, cache=True):
        if cache:
            return query_cache(self.__class__, pks=self.tn_ancestors_pks)
        else:
            return list(self.get_ancestors_queryset())

    def get_ancestors_count(self):
        return self.tn_ancestors_count

    def get_ancestors_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_ancestors_pks))

    def get_breadcrumbs(self, attr=None, cache=True):
        objs = self.get_ancestors(cache=cache) + [self]
        return [getattr(obj, attr) for obj in objs] if attr else objs

    def get_children(self, cache=True):
        if cache:
            return query_cache(self.__class__, pks=self.tn_children_pks)
        else:
            return list(self.get_children_queryset())

    def get_children_count(self):
        return self.tn_children_count

    def get_children_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_children_pks))

    def get_depth(self):
        return self.tn_depth

    def get_descendants(self, cache=True):
        if cache:
            return query_cache(self.__class__, pks=self.tn_descendants_pks)
        else:
            return list(self.get_descendants_queryset())

    def get_descendants_count(self):
        return self.tn_descendants_count

    def get_descendants_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_descendants_pks))

    def get_descendants_tree(self, cache=True):
        return self.__get_nodes_tree(instance=self, cache=cache)

    def get_descendants_tree_display(self, cache=True):
        objs = self.get_descendants(cache=cache)
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
        indentation = (mark * self.tn_ancestors_count) if indent else ''
        indentation = force_text(indentation)
        field_name = getattr(self, 'treenode_display_field', 'pk')
        text = getattr(self, field_name)
        text = force_text(text)
        return indentation + text

    def get_first_child(self, cache=True):
        return self.get_children(cache=cache)[0] \
            if self.get_children_count() else None

    def get_index(self):
        return self.tn_index

    def get_last_child(self, cache=True):
        return self.get_children(cache=cache)[-1] \
            if self.get_children_count() else None

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

    def get_root(self, cache=True):
        root_pk = (split_pks(self.tn_ancestors_pks) + [self.pk])[0]
        if cache:
            root_obj = query_cache(self.__class__, pk=root_pk)
        else:
            root_obj = self.__class__.objects.get(pk=root_pk)
        return root_obj

    @classmethod
    def get_roots(cls, cache=True):
        if cache:
            return [obj for obj in query_cache(cls) \
                if obj.tn_ancestors_count == 0]
        else:
            return list(cls.get_roots_queryset())

    @classmethod
    def get_roots_queryset(cls):
        return cls.objects.filter(tn_ancestors_count=0)

    def get_siblings(self, cache=True):
        if cache:
            return query_cache(self.__class__, pks=self.tn_siblings_pks)
        else:
            return list(self.get_siblings_queryset())

    def get_siblings_count(self):
        return self.tn_siblings_count

    def get_siblings_queryset(self):
        return self.__class__.objects.filter(
            pk__in=split_pks(self.tn_siblings_pks))

    @classmethod
    def get_tree(cls, cache=True):
        return cls.__get_nodes_tree(instance=None, cache=cache)

    @classmethod
    def get_tree_display(cls, cache=True):
        if cache:
            objs = query_cache(cls)
        else:
            objs = list(cls.objects.all())
        strs = ['%s' % (obj, ) for obj in objs]
        d = '\n'.join(strs)
        return d

    # @classmethod
    # def get_tree_dump(cls, cache=True, indent=2, default=None):
    #     data = cls.get_tree(cache=cache)
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

        debug_message_prefix = '[treenode] update %s.%s tree: ' % (
            cls.__module__, cls.__name__, )

        with debug_performance(debug_message_prefix):

            # update db
            objs_data = cls.__get_nodes_data()

            with transaction.atomic():
                for obj_key, obj_data in objs_data.items():
                    obj_pk = int(obj_key)
                    cls.objects.filter(pk=obj_pk).update(**obj_data)

            # update in-memory instances
            update_refs(cls, objs_data)

            # update cache instances
            update_cache(cls)

    # Private methods

    def __get_node_order_str(self):
        priority_max = 99999
        priority_len = len(str(priority_max))
        priority_val = priority_max - min(self.tn_priority, priority_max)
        priority_key = str(priority_val).zfill(priority_len)
        alphabetical_val = slugify(str(self))
        alphabetical_key = alphabetical_val.ljust(priority_len, str('z'))
        alphabetical_key = alphabetical_key[0:priority_len]
        pk_val = min(self.pk, priority_max)
        pk_key = str(pk_val).zfill(priority_len)
        s = '%s%s%s' % (priority_key, alphabetical_key, pk_key, )
        s = s.upper()
        return s

    def __get_node_data(self, objs_list, objs_dict):

        obj_dict = {}

        # update ancestors
        parent_pk = self.tn_parent_id

        ancestors_list = []
        ancestor_pk = parent_pk
        while ancestor_pk:
            ancestor_obj = objs_dict.get(str(ancestor_pk))
            ancestors_list.insert(0, ancestor_obj)
            ancestor_pk = ancestor_obj.tn_parent_id
        ancestors_pks = [obj.pk for obj in ancestors_list]
        ancestors_count = len(ancestors_pks)

        order_objs = list(ancestors_list) + [self]
        order_strs = [obj.__get_node_order_str() for obj in order_objs]
        order_str = ''.join(order_strs)[0:150]

        obj_dict = {
            'instance': self,
            'pk': self.pk,
            'tn_parent_pk': parent_pk,
            'tn_ancestors_pks': ancestors_pks,
            'tn_ancestors_count': ancestors_count,
            'tn_children_pks': [],
            'tn_children_count': 0,
            'tn_descendants_pks': [],
            'tn_descendants_count': 0,
            'tn_siblings_pks': [],
            'tn_siblings_count': 0,
            'tn_depth': 0,
            'tn_level': (ancestors_count + 1),
            'tn_order': 0,
            'tn_order_str': order_str,
        }

        return obj_dict

    @classmethod
    def __get_nodes_data(cls):

        objs_qs = cls.objects.select_related('tn_parent')
        objs_list = list(objs_qs)
        objs_dict = {str(obj.pk):obj for obj in objs_list}
        objs_data_dict = {str(obj.pk):obj.__get_node_data(objs_list, objs_dict) for obj in objs_list}
        objs_data_sort = lambda obj: objs_data_dict[str(obj['pk'])]['tn_order_str']
        objs_data_list = list(objs_data_dict.values())
        objs_data_list.sort(key=objs_data_sort)
        objs_pks_by_parent = {}
        objs_order_cursor = 0
        objs_index_cursors = {}
        objs_index_cursor = 0

        # index objects by parent pk
        for obj_data in objs_data_list:
            obj_parent_key = str(obj_data['tn_parent_pk'])
            if not obj_parent_key in objs_pks_by_parent:
                objs_pks_by_parent[obj_parent_key] = []
            objs_pks_by_parent[obj_parent_key].append(obj_data['pk'])

            # update global order with normalized value
            obj_data['tn_order'] = objs_order_cursor
            objs_order_cursor += 1

            # update child index
            obj_parent_key = str(obj_data['tn_parent_pk'])
            objs_index_cursor = objs_index_cursors.get(obj_parent_key, 0)
            obj_data['tn_index'] = objs_index_cursor
            objs_index_cursor += 1
            objs_index_cursors[obj_parent_key] = objs_index_cursor

        for obj_data in sorted(objs_data_list, key=lambda obj: obj['tn_level'], reverse=True):

            # update children
            children_parent_key = str(obj_data['pk'])
            obj_data['tn_children_pks'] = list(
                objs_pks_by_parent.get(children_parent_key, []))
            obj_data['tn_children_count'] = len(obj_data['tn_children_pks'])

            # update siblings
            siblings_parent_key = str(obj_data['tn_parent_pk'])
            obj_data['tn_siblings_pks'] = list(
                objs_pks_by_parent.get(siblings_parent_key, []))
            obj_data['tn_siblings_pks'].remove(obj_data['pk'])
            obj_data['tn_siblings_count'] = len(obj_data['tn_siblings_pks'])

            # update descendants and depth
            if obj_data['tn_children_count'] > 0:
                obj_children_pks = obj_data['tn_children_pks']
                obj_descendants_pks = list(obj_children_pks)
                obj_depth = 1
                for obj_child_pk in obj_children_pks:
                    obj_child_key = str(obj_child_pk)
                    obj_child_data = objs_data_dict[obj_child_key]
                    obj_child_descendants_pks = obj_child_data.get('tn_descendants_pks', [])
                    if obj_child_descendants_pks:
                        obj_descendants_pks += obj_child_descendants_pks
                        obj_depth = max(obj_depth, obj_child_data['tn_depth'] + 1)

                if obj_descendants_pks:
                    obj_descendants_sort = lambda obj_pk: objs_data_dict[str(obj_pk)]['tn_order']
                    obj_descendants_pks.sort(key=obj_descendants_sort)
                    obj_data['tn_descendants_pks'] = obj_descendants_pks
                    obj_data['tn_descendants_count'] = len(obj_data['tn_descendants_pks'])
                    obj_data['tn_depth'] = obj_depth

        for obj_data in objs_data_list:
            obj = obj_data['instance']
            obj_key = str(obj_data['pk'])

            # join all pks lists
            obj_data['tn_ancestors_pks'] = join_pks(obj_data['tn_ancestors_pks'])
            obj_data['tn_children_pks'] = join_pks(obj_data['tn_children_pks'])
            obj_data['tn_descendants_pks'] = join_pks(obj_data['tn_descendants_pks'])
            obj_data['tn_siblings_pks'] = join_pks(obj_data['tn_siblings_pks'])

            # clean data
            obj_data.pop('instance', None)
            obj_data.pop('pk', None)
            obj_data.pop('tn_parent_pk', None)
            obj_data.pop('tn_order_str', None)

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
                objs_data_dict.pop(obj_key, None)

        return objs_data_dict

    @classmethod
    def __get_nodes_tree(cls, instance=None, cache=True):

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
            objs_pks = instance.tn_descendants_pks
            if cache:
                objs_list = query_cache(cls, pks=objs_pks)
            else:
                objs_list = list(cls.objects.filter(pk__in=split_pks(objs_pks)))
            objs_dict = { str(obj.pk):obj for obj in objs_list }
            objs_tree = __get_node_tree(instance)['tree']
        else:
            if cache:
                objs_list = query_cache(cls)
            else:
                objs_list = list(cls.objects.all())
            objs_dict = { str(obj.pk):obj for obj in objs_list }
            objs_tree = [__get_node_tree(obj)
                        for obj in objs_list if obj.tn_level == 1]

        return objs_tree

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
    def breadcrumbs(self):
        return self.get_breadcrumbs()

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
    def first_child(self):
        return self.get_first_child()

    @property
    def index(self):
        return self.get_index()

    @property
    def last_child(self):
        return self.get_last_child()

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

    class Meta:
        abstract = True
        ordering = ['tn_order']

    def __str__(self):
        return self.get_display(indent=True)

connect_signals()
