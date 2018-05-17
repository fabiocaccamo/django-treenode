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
