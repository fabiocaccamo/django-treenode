# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from treenode.models import TreeNodeModel, TreeNodeProperties


class Category(TreeNodeModel, TreeNodeProperties):

    treenode_display_field = 'name'

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
