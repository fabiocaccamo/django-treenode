import random
import string
import uuid
from abc import ABCMeta, abstractmethod

from django.db import models
from django.db.models.base import ModelBase

from treenode.models import TreeNodeModel


class Category(TreeNodeModel):
    treenode_display_field = "name"

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CategoryFixtures(TreeNodeModel):
    treenode_display_field = "name"

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category Fixtures"
        verbose_name_plural = "Categories Fixtures"


class CategoryWithStringPk(TreeNodeModel):
    treenode_display_field = "name"

    @staticmethod
    def get_random_string():
        return "".join(random.choice(string.letters + string.digits) for n in range(64))

    id = models.CharField(
        primary_key=True, max_length=100, default=get_random_string, editable=False
    )
    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CategoryWithUUIDPk(TreeNodeModel):
    treenode_display_field = "name"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CategoryWithoutDisplayField(TreeNodeModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class _ABCMetaModelBase(ABCMeta, ModelBase):
    """Metaclass combining Python's ABCMeta with Django's ModelBase."""

    pass


class AbstractCategoryProxy(Category, metaclass=_ABCMetaModelBase):
    """
    A Django proxy model that is also a Python ABC.

    Used to reproduce issue #215: post_migrate_treenode calls update_tree()
    on this model even though it cannot be instantiated.
    """

    class Meta:
        app_label = "tests"
        proxy = True

    @abstractmethod
    def my_method(self):
        """Subclasses must implement this."""
        ...
