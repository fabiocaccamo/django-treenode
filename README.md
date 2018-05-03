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
- **Fast** - get model `children`, `depth`, `index`, `level`, `parents`, `root`, `siblings`, `tree`, and much more... *(max 1 query)*
- **Synced** - in-memory model instances are automatically updated *(0 queries)*
- **Compatibility** - you can easily add treenode to existing projects
- **Easy configuration** - just extend the abstract model / model-admin
- **Admin integration** - great tree visualization with optional accordion
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

    # the field used to display the model instance
    # default value 'pk'
    treenode_display_field = 'name'

    name = models.CharField(max_length=50)

    class Meta(TreeNodeModel.Meta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
```

Now many fields *(used internally to speed-up operations)* have been added to your model,
and many public methods are available.

All `TreeNodeModel` fields are prefixed with `tn_` to prevent direct access and avoid conflicts with possible existing fields.

If you want to access public methods as properties just make your model inherit from both `treenode.models.TreenodeModel` and `treenode.models.TreenodeProperties`:

```python
# ...

from treenode.models import TreeNodeModel, TreeNodeProperties


class Category(TreeNodeModel, TreeNodeProperties):

    # ...
```

#### `admin.py`
Make your model-admin class inherit from `TreeNodeModelAdmin`.

```python
from django.contrib import admin

from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreenodeForm

from .models import Category


class CategoryAdmin(TreeNodeModelAdmin):

    # if True an accordion will be used in the changelist view
    # default value False
    treenode_accordion = True

    # use TreenodeForm to automatically exclude invalid parent choices
    form = TreenodeForm

admin.site.register(Category, CategoryAdmin)
```

## Usage
The following methods/properties will be available on your model instances:

### Methods/Properties:
*Note that properties are available only if your model implements* `treenode.models.TreeNodeProperties` *for more info check the configuration section)*

Return a list containing all children *(1 query)*:
```python
instance.get_children()
# or
instance.children
```

Return the children count *(0 queries)*:
```python
instance.get_children_count()
# or
instance.children_count
```

Return the children queryset *(0 queries)*:
```python
instance.get_children_queryset()
```

Return the node depth (how many levels of descendants) *(0 queries)*:
```python
instance.get_depth()
# or
instance.depth
```

Return a list containing all descendants *(1 query)*:
```python
instance.get_descendants()
# or
instance.descendants
```

Return the descendants count *(0 queries)*:
```python
instance.get_descendants_count()
# or
instance.descendants_count
```

Return the descendants queryset *(0 queries)*:
```python
instance.get_descendants_queryset()
```

Return a n-dimensional `dict` representing the model tree starting from the current node *(1 query)*:
```python
instance.get_descendants_tree()
# or
instance.descendants_tree
```

Return a multiline string representing the model tree starting from the current node *(1 query)*:
```python
instance.get_descendants_tree_display()
# or
instance.descendants_tree_display
```

Return the node index (index in node.parent.children list) *(0 queries)*:
```python
instance.get_index()
# or
instance.index
```

Return the node level (starting from 1) *(0 queries)*:
```python
instance.get_level()
# or
instance.level
```

Return the order value used for ordering *(0 queries)*:
```python
instance.get_order()
# or
instance.order
```

Return the parent node *(1 query)*:
```python
instance.get_parent()
# or
instance.parent
```

Return a list with all parents ordered from root to parent *(1 query)*:
```python
instance.get_parents()
# or
instance.parents
```

Return the parents count *(0 queries)*:
```python
instance.get_parents_count()
# or
instance.parents_count
```

Return the parents queryset *(0 queries)*:
```python
instance.get_parents_queryset()
```

Return the node priority *(0 queries)*:
```python
instance.get_priority()
# or
instance.priority
```

Return the root node for the current node *(1 query)*:
```python
instance.get_root()
# or
instance.root
```

Return all root nodes *(1 query)*:
```python
cls.get_roots()
# or
cls.roots
```

Return a list with all the siblings *(1 query)*:
```python
instance.get_siblings()
# or
instance.siblings
```

Return the siblings count *(0 queries)*:
```python
instance.get_siblings_count()
# or
instance.siblings_count
```

Return the siblings queryset *(0 queries)*:
```python
instance.get_siblings_queryset()
```

Return a n-dimensional `dict` representing the model tree *(1 query)*:
```python
cls.get_tree()
# or
cls.tree
```

Return a multiline string representing the model tree *(1 query)*:
```python
cls.get_tree_display()
# or
cls.tree_display
```

Return `True` if the current node is the first child *(0 queries)*:
```python
instance.is_first_child()
```

Return `True` if the current node is the last child *(0 queries)*:
```python
instance.is_last_child()
```

### Update tree manually:
Useful after bulk updates:
```python
cls.update_tree()
```

## License
Released under [MIT License](LICENSE.txt).
