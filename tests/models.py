import random
import string
import uuid

from django.db import models

from treenode.models import TreeNodeModel


class Category(TreeNodeModel):
    treenode_display_field = "name"

    name = models.CharField(max_length=50, unique=True)

    class Meta(TreeNodeModel.Meta):
        app_label = "tests"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


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
