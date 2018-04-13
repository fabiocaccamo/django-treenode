[![Build Status](https://travis-ci.org/fabiocaccamo/django-treenode.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-treenode)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-treenode/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-treenode)
[![Code Health](https://landscape.io/github/fabiocaccamo/django-treenode/master/landscape.svg?style=flat)](https://landscape.io/github/fabiocaccamo/django-treenode/master)
[![Requirements Status](https://requires.io/github/fabiocaccamo/django-treenode/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/django-treenode/requirements/?branch=master)
[![PyPI version](https://badge.fury.io/py/django-treenode.svg)](https://badge.fury.io/py/django-treenode)
[![Py versions](https://img.shields.io/pypi/pyversions/django-treenode.svg)](https://img.shields.io/pypi/pyversions/django-treenode.svg)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

# django-treenode
Probably the best abstract model for your tree based stuff.

## Requirements
- Python 2.7, 3.4, 3.5, 3.6
- Django 1.8, 1.9, 1.10, 1.11, 2.0

## Installation
- Run ``pip install django-treenode``

## Usage

#### Models
Make your model class inherit from `TreeNodeModel`:


```python
from django.db import models

from treenode.models import TreeNodeModel


class Category(TreeNodeModel):

    name = models.CharField(max_length=50)

    class Meta(TreeNodeModel.Meta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.get_display(self.name)
```

#### Admin
Make your model-admin class inherit from `TreeNodeModelAdmin`:

```python
from django.contrib import admin

from treenode.admin import TreeNodeModelAdmin

from .models import Category


class CategoryAdmin(TreeNodeModelAdmin):

    list_display = ('name_display', )

    def name_display(self, obj):
        return self.get_treenode_display(obj, obj.name, accordion=True)

    name_display.short_description = 'Name'
    name_display.allow_tags = True

admin.site.register(Category, CategoryAdmin)
```

## License
Released under [MIT License](LICENSE.txt).
