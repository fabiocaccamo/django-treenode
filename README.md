[![Build Status](https://travis-ci.org/fabiocaccamo/django-treenode.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-treenode)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-treenode/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-treenode)
[![Code Health](https://landscape.io/github/fabiocaccamo/django-treenode/master/landscape.svg?style=flat)](https://landscape.io/github/fabiocaccamo/django-treenode/master)
[![Requirements Status](https://requires.io/github/fabiocaccamo/django-treenode/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/django-treenode/requirements/?branch=master)
[![PyPI version](https://badge.fury.io/py/django-treenode.svg)](https://badge.fury.io/py/django-treenode)
[![PyPI downloads](https://img.shields.io/pypi/dm/django-treenode.svg)](https://img.shields.io/pypi/dm/django-treenode.svg)
[![Py versions](https://img.shields.io/pypi/pyversions/django-treenode.svg)](https://img.shields.io/pypi/pyversions/django-treenode.svg)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

[simple-admin]: https://user-images.githubusercontent.com/1035294/39823224-dff5944c-53ac-11e8-9d7f-60f1a31b2730.png
[accordion-admin]: https://user-images.githubusercontent.com/1035294/39823232-e3a5d99e-53ac-11e8-98ad-edd6b77c44a4.png

# django-treenode
Probably the best abstract model / admin for your **tree** based stuff.

## Features
- **Fast** - get `ancestors`, `children`, `descendants`, `parent`, `root`, `siblings`, `tree` with **no queries**
- **Synced** - in-memory model instances are automatically updated
- **Compatibility** - you can easily add treenode to existing projects
- **No dependencies**
- **Easy configuration** - just extend the abstract model / model-admin
- **Admin integration** - great tree visualization: accordion, breadcrumbs or indentation

| Simple admin | Accordion admin |
| --- | --- |
| ![simple-admin][simple-admin] | ![accordion-admin][accordion-admin] |

## Requirements
- Python 2.7, 3.4, 3.5, 3.6, 3.7
- Django 1.8, 1.9, 1.10, 1.11, 2.0, 2.1

## Installation
- Run `pip install django-treenode`
- Add `treenode` to `settings.INSTALLED_APPS`
- Make your model inherit from `treenode.models.TreeNodeModel` *(described below)*
- Make your model-admin inherit from `treenode.admin.TreeNodeModelAdmin` *(described below)*
- Run `python manage.py makemigrations` and `python manage.py migrate`

## Configuration
#### `models.py`
Make your model class inherit from `treenode.models.TreeNodeModel`:

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

The `TreeNodeModel` abstract class adds many fields (prefixed with `tn_` to prevent direct access) and public methods to your models.

---

#### `admin.py`
Make your model-admin class inherit from `treenode.admin.TreeNodeModelAdmin`.

```python
from django.contrib import admin

from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm

from .models import Category


class CategoryAdmin(TreeNodeModelAdmin):

    # set the changelist display mode: 'accordion', 'breadcrumbs' or 'indentation' (default)
    # when changelist results are filtered by a querystring,
    # 'breadcrumbs' mode will be used (to preserve data display integrity)
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION

    # use TreeNodeForm to automatically exclude invalid parent choices
    form = TreeNodeForm

admin.site.register(Category, CategoryAdmin)
```

## Usage

#### Methods/Properties:

**Delete a node** and all its descendants:
```python
obj.delete()
```

**Delete the whole tree** for the current node class:
```python
cls.delete_tree()
```

Get a **list with all ancestors** (ordered from root to parent):
```python
obj.get_ancestors()
# or
obj.ancestors
```

Get the **ancestors count**:
```python
obj.get_ancestors_count()
# or
obj.ancestors_count
```

Get the **ancestors queryset**:
```python
obj.get_ancestors_queryset()
```

Get the **breadcrumbs** to current node (included):
```python
obj.get_breadcrumbs(attr=None)
# or
obj.breadcrumbs
```

Get a **list containing all children**:
```python
obj.get_children()
# or
obj.children
```

Get the **children count**:
```python
obj.get_children_count()
# or
obj.children_count
```

Get the **children queryset**:
```python
obj.get_children_queryset()
```

Get the **node depth** (how many levels of descendants):
```python
obj.get_depth()
# or
obj.depth
```

Get a **list containing all descendants**:
```python
obj.get_descendants()
# or
obj.descendants
```

Get the **descendants count**:
```python
obj.get_descendants_count()
# or
obj.descendants_count
```

Get the **descendants queryset**:
```python
obj.get_descendants_queryset()
```

Get a **n-dimensional** `dict` representing the **model tree**:
```python
obj.get_descendants_tree()
# or
obj.descendants_tree
```

Get a **multiline** `string` representing the **model tree**:
```python
obj.get_descendants_tree_display()
# or
obj.descendants_tree_display
```

Get the **first child node**:
```python
obj.get_first_child()
# or
obj.first_child
```

Get the **node index** (index in node.parent.children list):
```python
obj.get_index()
# or
obj.index
```

Get the **last child node**:
```python
obj.get_last_child()
# or
obj.last_child
```

Get the **node level** (starting from 1):
```python
obj.get_level()
# or
obj.level
```

Get the **order value** used for ordering:
```python
obj.get_order()
# or
obj.order
```

Get the **parent node**:
```python
obj.get_parent()
# or
obj.parent
```

Set the **parent node**:
```python
obj.set_parent(parent_obj)
```

Get the **node priority**:
```python
obj.get_priority()
# or
obj.priority
```

Set the **node priority**:
```python
obj.set_priority(100)
```

Get the **root node** for the current node:
```python
obj.get_root()
# or
obj.root
```

Get a **list with all root nodes**:
```python
cls.get_roots()
# or
cls.roots
```

Get **root nodes queryset**:
```python
cls.get_roots_queryset()
```

Get a **list with all the siblings**:
```python
obj.get_siblings()
# or
obj.siblings
```

Get the **siblings count**:
```python
obj.get_siblings_count()
# or
obj.siblings_count
```

Get the **siblings queryset**:
```python
obj.get_siblings_queryset()
```

Get a **n-dimensional** `dict` representing the **model tree**:
```python
cls.get_tree()
# or
cls.tree
```

Get a **multiline** `string` representing the **model tree**:
```python
cls.get_tree_display()
# or
cls.tree_display
```

Return `True` if the current node **is ancestor** of target_obj:
```python
obj.is_ancestor_of(target_obj)
```

Return `True` if the current node **is child** of target_obj:
```python
obj.is_child_of(target_obj)
```

Return `True` if the current node **is descendant** of target_obj:
```python
obj.is_descendant_of(target_obj)
```

Return `True` if the current node is the **first child**:
```python
obj.is_first_child()
```

Return `True` if the current node is the **last child**:
```python
obj.is_last_child()
```

Return `True` if the current node is **leaf** (it has not children):
```python
obj.is_leaf()
```

Return `True` if the current node **is parent** of target_obj:
```python
obj.is_parent_of(target_obj)
```

Return `True` if the current node **is root**:
```python
obj.is_root()
```

Return `True` if the current node **is root** of target_obj:
```python
obj.is_root_of(target_obj)
```

Return `True` if the current node **is sibling** of target_obj:
```python
obj.is_sibling_of(target_obj)
```

**Update tree** manually, useful after **bulk updates**:
```python
cls.update_tree()
```

## License
Released under [MIT License](LICENSE.txt).
