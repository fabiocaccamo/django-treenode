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
