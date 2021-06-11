# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.db import models

from treenode.models import TreeNodeModel


class Category(TreeNodeModel):
    treenode_display_field = 'name'

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryUUID(TreeNodeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    treenode_display_field = 'name'

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
