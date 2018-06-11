# -*- coding: utf-8 -*-

from collections import defaultdict

import weakref


__refs__ = defaultdict(weakref.WeakSet)


def clear_refs(cls):
    __refs__[cls].clear()


def get_refs(cls):
    return __refs__[cls]


def set_ref(cls, obj):
    if obj.pk:
        __refs__[cls].add(obj)


def update_refs(cls, data):
    for obj in get_refs(cls):
        obj_key = str(obj.pk)
        obj_data = data.get(obj_key)
        if obj_data:
            for key, value in obj_data.items():
                setattr(obj, key, value)
