[![Build Status](https://travis-ci.org/fabiocaccamo/django-treenode.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-treenode)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-treenode/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-treenode)
[![Code Health](https://landscape.io/github/fabiocaccamo/django-treenode/master/landscape.svg?style=flat)](https://landscape.io/github/fabiocaccamo/django-treenode/master)
[![Requirements Status](https://requires.io/github/fabiocaccamo/django-treenode/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/django-treenode/requirements/?branch=master)
[![PyPI version](https://badge.fury.io/py/django-treenode.svg)](https://badge.fury.io/py/django-treenode)
[![Py versions](https://img.shields.io/pypi/pyversions/django-treenode.svg)](https://img.shields.io/pypi/pyversions/django-treenode.svg)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

# django-treenode
Probably the best abstract model for your tree based stuff.

## Features
- **Fast:** get model `tree`, `root`, `parent`, `parents`, `children`, `children_tree`, `siblings`, `level`, `index`, `depth` with **max 1 query**
- **Zero configuration:** just extend the abstract model
- **Admin integration**
- **No dependencies**

## Requirements
- Python 2.7, 3.4, 3.5, 3.6
- Django 1.8, 1.9, 1.10, 1.11, 2.0

## Installation
- Run `pip install django-treenode`
- Make your model inherit from `treenode.models.TreeNodeModel` *(described below)*
- Make your model-admin inherit from `treenode.admin.TreeNodeModelAdmin` *(described below)*
- Run `python manage.py makemigrations` and `python manage.py migrate`

## Configuration
#### `models.py`
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
        return self.get_display_text(self.name)
```

#### `admin.py`
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

## Usage
Now your models have some extra fields used by `django-treenode` to speed-up tree operations.
The following properties will be accessible on your model instances:

```python
# return a n-dimensional dict representing the model tree (1 query)
instance.tree
```

```python
# return all the root nodes (1 query)
instance.roots
```

```python
# return the root node (1 query)
instance.root
```

```python
# return the parent node (1 query)
instance.parent
```

```python
# return a list with all the parents ordered from root to parent (1 query)
instance.parents
```

```python
# return the parents count (0 queries)
instance.parents_count
```

```python
# return a list with all the children (1 query)
instance.children
```

```python
# return the children count (0 queries)
instance.children_count
```

```python
# return a n-dimensional dict representing the model tree starting from the current node (1 query)
instance.children_tree
```

```python
# return a list with all the siblings (1 query)
instance.siblings
```

```python
# return the siblings count (0 queries)
instance.siblings_count
```

```python
# return the node level (0 queries)
instance.level
```

```python
# return the node index in parent.children list (0 queries)
instance.index
```

```python
# return the node depth (0 queries)
instance.depth
```

```python
# return the order value used for sorting nodes (0 queries)
instance.order
```

## License
Released under [MIT License](LICENSE.txt).
