[![](https://img.shields.io/pypi/pyversions/django-treenode.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/djversions/django-treenode?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)

[![](https://img.shields.io/pypi/v/django-treenode.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-treenode/)
[![](https://pepy.tech/badge/django-treenode)](https://pepy.tech/project/django-treenode)
[![](https://img.shields.io/github/stars/fabiocaccamo/django-treenode?logo=github)](https://github.com/fabiocaccamo/django-treenode/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/django-treenode?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/django-treenode.svg?color=blue)](https://github.com/fabiocaccamo/django-treenode/blob/master/LICENSE.txt)

[![](https://img.shields.io/github/workflow/status/fabiocaccamo/django-treenode/Python%20package?label=build&logo=github)](https://github.com/fabiocaccamo/django-treenode)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/django-treenode?logo=codecov)](https://codecov.io/gh/fabiocaccamo/django-treenode)
[![](https://img.shields.io/codacy/grade/0c79c196e5c9411babbaf5e8e5f7469c?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/django-treenode)
[![](https://requires.io/github/fabiocaccamo/django-treenode/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/django-treenode/requirements/?branch=master)

# django-treenode
Probably the best abstract model / admin for your **tree** based stuff.

## Features
-   **Fast** - get `ancestors`, `children`, `descendants`, `parent`, `root`, `siblings`, `tree` with **no queries**
-   **Synced** - in-memory model instances are automatically updated
-   **Compatibility** - you can easily add `treenode` to existing projects
-   **No dependencies**
-   **Easy configuration** - just extend the abstract model / model-admin
-   **Admin integration** - great tree visualization: **accordion**, **breadcrumbs** or **indentation**

| indentation (default) | breadcrumbs | accordion |
| --- | --- | --- |
| ![treenode-admin-display-mode-indentation][treenode-admin-display-mode-indentation] | ![treenode-admin-display-mode-breadcrumbs][treenode-admin-display-mode-breadcrumbs] | ![treenode-admin-display-mode-accordion][treenode-admin-display-mode-accordion] |

## Installation
-   Run `pip install django-treenode`
-   Add `treenode` to `settings.INSTALLED_APPS`
-   Make your model inherit from `treenode.models.TreeNodeModel` *(described below)*
-   Make your model-admin inherit from `treenode.admin.TreeNodeModelAdmin` *(described below)*
-   Run `python manage.py makemigrations` and `python manage.py migrate`

## Configuration
### `models.py`
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

:warning: **If you are extending a model that already has some fields, please ensure that your model existing fields names don't clash with `TreeNodeModel` public [methods/properties](#methodsproperties) names.**

---

### `admin.py`
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
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION

    # use TreeNodeForm to automatically exclude invalid parent choices
    form = TreeNodeForm

admin.site.register(Category, CategoryAdmin)
```

---

### `settings.py`
You can use a custom cache backend by adding a `treenode` entry to `settings.CACHES`, otherwise the default cache backend will be used.

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '...',
    },
    'treenode': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
```

## Usage

### Methods/Properties

**Delete a node** if `cascade=True` (default behaviour), children and descendants will be deleted too,
otherwise children's parent will be set to `None` (then children become roots):
```python
obj.delete(cascade=True)
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

Get the **ancestors pks** list:
```python
obj.get_ancestors_pks()
# or
obj.ancestors_pks
```

Get the **ancestors queryset** (ordered from parent to root):
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

Get the **children pks** list:
```python
obj.get_children_pks()
# or
obj.children_pks
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

Get the **descendants pks** list:
```python
obj.get_descendants_pks()
# or
obj.descendants_pks
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

Get the **parent node pk**:
```python
obj.get_parent_pk()
# or
obj.parent_pk
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

Get the **root node pk** for the current node:
```python
obj.get_root_pk()
# or
obj.root_pk
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

Get the **siblings pks** list:
```python
obj.get_siblings_pks()
# or
obj.siblings_pks
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

### Bulk Operations

To perform bulk operations it is recommended to turn off signals, then triggering the tree update at the end:

```python
from treenode.signals import no_signals

with no_signals():
    # execute custom bulk operations
    pass

# trigger tree update only once
YourModel.update_tree()
```

## Testing
```bash
# create python virtual environment
virtualenv testing_django_treenode

# activate virtualenv
cd testing_django_treenode && . bin/activate

# clone repo
git clone https://github.com/fabiocaccamo/django-treenode.git src && cd src

# install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# run tests
tox
# or
python setup.py test
# or
python -m django test --settings "tests.settings"
```

## License
Released under [MIT License](LICENSE.txt).

---

## See also

- [`django-admin-interface`](https://github.com/fabiocaccamo/django-admin-interface) - the default admin interface made customizable by the admin itself. popup windows replaced by modals. 🧙 ⚡

- [`django-colorfield`](https://github.com/fabiocaccamo/django-colorfield) - simple color field for models with a nice color-picker in the admin. 🎨

- [`django-extra-settings`](https://github.com/fabiocaccamo/django-extra-settings) - config and manage typed extra settings using just the django admin. ⚙️

- [`django-maintenance-mode`](https://github.com/fabiocaccamo/django-maintenance-mode) - shows a 503 error page when maintenance-mode is on. 🚧 🛠️

- [`django-redirects`](https://github.com/fabiocaccamo/django-redirects) - redirects with full control. ↪️

- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘

- [`python-codicefiscale`](https://github.com/fabiocaccamo/python-codicefiscale) - encode/decode Italian fiscal codes - codifica/decodifica del Codice Fiscale. 🇮🇹 💳

- [`python-fontbro`](https://github.com/fabiocaccamo/python-fontbro) - friendly font operations. 🧢

- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️

[treenode-admin-display-mode-accordion]: https://user-images.githubusercontent.com/1035294/54942407-5040ec00-4f2f-11e9-873b-d0b3b521f534.png
[treenode-admin-display-mode-breadcrumbs]: https://user-images.githubusercontent.com/1035294/54942410-50d98280-4f2f-11e9-8a8b-a1ac6208398a.png
[treenode-admin-display-mode-indentation]: https://user-images.githubusercontent.com/1035294/54942411-50d98280-4f2f-11e9-9daf-d8339dd7a159.png
