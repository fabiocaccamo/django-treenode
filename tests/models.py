# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from treenode.models import TreeNodeModel

import uuid


class Category(TreeNodeModel):

    treenode_display_field = 'name'

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryUUID(TreeNodeModel):

    treenode_display_field = 'name'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryStr(TreeNodeModel):

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class CategoryUUIDStr(TreeNodeModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

class CategoryPk(TreeNodeModel):

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
