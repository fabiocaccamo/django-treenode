# -*- coding: utf-8 -*-

from collections import defaultdict

import weakref


__refs__ = defaultdict(weakref.WeakSet)


def clear_refs(cls):
    __refs__[cls].clear()


def get_refs(cls):
    # print(len(__refs__[cls]))
    return __refs__[cls]


def set_ref(cls, obj):
    if obj.pk:
        __refs__[cls].add(obj)


# __refs__ = defaultdict(list)


# def clear_refs(cls):
#     __refs__[cls][:] = []


# def get_refs(cls):
#     refs = []
#     for ref in __refs__[cls]:
#         obj = ref()
#         if obj is not None:
#             refs.append(ref)
#             yield obj
#     # print(len(refs))
#     __refs__[cls] = refs


# def set_ref(cls, obj):
#     if obj.pk:
#         ref = weakref.ref(obj)
#         __refs__[cls].append(ref)
