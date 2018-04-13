# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from treenode.models import TreeNodeModel


@python_2_unicode_compatible
class Category(TreeNodeModel):

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = 'tests'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_display_text(self.name)
