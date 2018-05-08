# -*- coding: utf-8 -*-

from collections import defaultdict

import weakref


# __refs__ = defaultdict(weakref.WeakSet)
__refs__ = defaultdict(list)


def get_refs(cls):
    # return __refs__[cls]
    refs = []
    for ref in __refs__[cls]:
        instance = ref()
        if instance is not None:
            refs.append(ref)
            yield instance
    # print(len(refs))
    __refs__[cls] = refs


def set_ref(instance):
    # if instance.pk:
    #     cls = instance.__class__
    #     __refs__[cls].add(instance)
    if instance.pk:
        cls = instance.__class__
        ref = weakref.ref(instance)
        __refs__[cls].append(ref)
